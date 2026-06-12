import ast
import datetime
import os

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated")


def _ensure_generated_dir():
    os.makedirs(GENERATED_DIR, exist_ok=True)


def docstring_generate(file_path: str) -> str:
    if not os.path.isfile(file_path):
        return f"File not found: {file_path}"

    try:
        from modules.llm.openrouter_client import ask_llm

        with open(file_path) as f:
            content = f.read()
        prompt = (
            "Add Google-style docstrings to all functions and classes in this Python code. "
            f"Return only the complete code with docstrings.\n\n{content}"
        )
        result = ask_llm(prompt)
        if result:
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"docs_{os.path.basename(file_path)}"
            fpath = os.path.join(GENERATED_DIR, fname)
            with open(fpath, "w") as f:
                f.write(result)
            return f"Docstringed code -> {fpath}"
    except Exception:
        pass

    # fallback: add minimal docstrings
    with open(file_path) as f:
        source = f.read()

    tree = ast.parse(source)
    lines = source.split("\n")
    inserts = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (not ast.get_docstring(node)) and node.body:
                indent = (
                    " " * (node.col_offset + 4)
                    if hasattr(node, "col_offset")
                    else "    "
                )
                doc = f'{indent}"""{node.name}"""'
                inserts.append((node.body[0].lineno - 1, doc))

    inserts.sort(key=lambda x: x[0], reverse=True)
    for lineno, doc in inserts:
        lines.insert(lineno, doc)

    result = "\n".join(lines)
    datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"docs_{os.path.basename(file_path)}"
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w") as f:
        f.write(result)
    return f"Minimal docstrings added -> {fpath}"


def readme_generate(project_path: str = ".") -> str:
    _ensure_generated_dir()

    try:
        from modules.llm.openrouter_client import ask_llm

        files = os.listdir(project_path)
        prompt = (
            f"Create a README.md for a project with these files: {', '.join(files[:20])}. "
            "Include: project overview, setup, usage. Return only markdown."
        )
        md = ask_llm(prompt)
        if md:
            fpath = os.path.join(GENERATED_DIR, "README.md")
            with open(fpath, "w") as f:
                f.write(md)
            return f"README generated -> {fpath}"
    except Exception:
        pass

    md = (
        "# Project\n\n"
        f"Auto-generated README for {os.path.abspath(project_path)}\n\n"
        "## Setup\n\n1. Install dependencies\n"
        "2. Run `python main.py`\n\n"
        "## Usage\n\nRefer to code documentation.\n"
    )
    fpath = os.path.join(GENERATED_DIR, "README.md")
    with open(fpath, "w") as f:
        f.write(md)
    return f"Template README -> {fpath}"
