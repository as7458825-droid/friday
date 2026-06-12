import hashlib
import json
import os
import subprocess

MANIFEST_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "integrity_manifest.json"
)
CORE_EXTENSIONS = {".py"}
CORE_DIRS = {"core", "advanced", "config.py", "main.py"}
HASHER_EXE = os.path.join(os.path.dirname(__file__), "FastHasher.exe")


def generate_file_hash(filepath: str, algorithm: str = "sha256") -> str:
    # Try C++ FastHasher First (High Performance)
    if os.path.exists(HASHER_EXE):
        try:
            process = subprocess.Popen(
                [HASHER_EXE, filepath],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, _ = process.communicate()
            if "RESULT:" in stdout:
                return stdout.split("RESULT:")[1].strip()
        except Exception:
            pass

    # Fallback to Python standard library
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def create_manifest(directory: str = ".") -> list[dict]:
    entries = []
    for root, dirs, files in os.walk(directory):
        if ".git" in dirs:
            dirs.remove(".git")
        if "venv" in dirs:
            dirs.remove("venv")
        for fname in files:
            if fname.endswith(".pyc"):
                continue
            fpath = os.path.join(root, fname)
            entries.append(
                {
                    "path": os.path.relpath(fpath, directory),
                    "hash": generate_file_hash(fpath),
                }
            )
    with open(MANIFEST_FILE, "w") as f:
        json.dump(entries, f, indent=2)
    return entries


def verify_integrity(directory: str = ".") -> str:
    if not os.path.isfile(MANIFEST_FILE):
        return "No manifest found. Run create_manifest first."

    with open(MANIFEST_FILE) as f:
        manifest = json.load(f)

    changed = []
    missing = []
    for entry in manifest:
        fpath = os.path.join(directory, entry["path"])
        if not os.path.isfile(fpath):
            missing.append(entry["path"])
        else:
            current = generate_file_hash(fpath)
            if current != entry["hash"]:
                changed.append(entry["path"])

    parts = []
    if changed:
        parts.append(f"{len(changed)} file(s) changed: {', '.join(changed[:5])}")
    if missing:
        parts.append(f"{len(missing)} file(s) missing: {', '.join(missing[:5])}")
    if not changed and not missing:
        parts.append("All files intact.")

    return ". ".join(parts)
