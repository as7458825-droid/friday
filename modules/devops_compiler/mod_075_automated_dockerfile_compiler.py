import datetime
import os

from jinja2 import Template

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated")

DOCKERFILE_PYTHON = Template("""FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "{{ entrypoint }}"]
""")

DOCKERFILE_NODE = Template("""FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE {{ port }}

CMD ["node", "{{ entrypoint }}"]
""")

DOCKERFILE_GO = Template("""FROM golang:1.22-alpine AS build

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o /app/server .

FROM alpine:latest
COPY --from=build /app/server /server
CMD ["/server"]
""")


def _ensure_generated_dir():
    os.makedirs(GENERATED_DIR, exist_ok=True)


def _write_dockerfile(content: str) -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"Dockerfile_{ts}"
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w") as f:
        f.write(content)
    return fpath


def generate_dockerfile(
    language: str = "python", dependencies: list[str] | None = None
) -> str:
    _ensure_generated_dir()

    lang = language.lower()
    entrypoint = (
        "main.py"
        if lang == "python"
        else "index.js"
        if lang in ("node", "nodejs")
        else "main.go"
    )

    if lang in ("python", "flask", "fastapi", "django"):
        content = DOCKERFILE_PYTHON.render(entrypoint=entrypoint)
    elif lang in ("node", "nodejs", "javascript", "typescript"):
        content = DOCKERFILE_NODE.render(entrypoint=entrypoint, port=3000)
    elif lang == "go" or lang == "golang":
        content = DOCKERFILE_GO.render()
    else:
        content = DOCKERFILE_PYTHON.render(entrypoint=entrypoint)

    fpath = _write_dockerfile(content)
    return f"Dockerfile generated -> {fpath}"


def build_image(dockerfile_path: str = None, tag: str = "friday-app:latest") -> str:
    if dockerfile_path is None:
        candidates = [
            f for f in os.listdir(GENERATED_DIR) if f.startswith("Dockerfile_")
        ]
        if not candidates:
            return "No Dockerfile found. Generate one first."
        dockerfile_path = os.path.join(GENERATED_DIR, sorted(candidates)[-1])

    try:
        import docker

        client = docker.from_env()
        image, logs = client.images.build(
            path=os.path.dirname(dockerfile_path), dockerfile=dockerfile_path, tag=tag
        )
        return f"Image {tag} built successfully"
    except ImportError:
        return "docker-py not installed. Run: pip install docker"
    except Exception as e:
        return f"Docker build failed: {e}"
