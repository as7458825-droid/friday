import os

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "file_audit.json"
)


def sort_folder(folder_path: str) -> str:
    import shutil

    if not os.path.isdir(folder_path):
        return "Folder not found."
    moved = 0
    for f in os.listdir(folder_path):
        fp = os.path.join(folder_path, f)
        if os.path.isfile(fp):
            ext = f.split(".")[-1] if "." in f else "no_ext"
            target = os.path.join(folder_path, ext.upper())
            os.makedirs(target, exist_ok=True)
            shutil.move(fp, os.path.join(target, f))
            moved += 1
    return f"Moved {moved} files into category folders."


def bulk_rename(folder: str, prefix: str) -> str:
    import os

    count = 0
    for i, f in enumerate(os.listdir(folder)):
        fp = os.path.join(folder, f)
        if os.path.isfile(fp):
            ext = f.split(".")[-1] if "." in f else ""
            new = f"{prefix}_{i + 1}.{ext}" if ext else f"{prefix}_{i + 1}"
            os.rename(fp, os.path.join(folder, new))
            count += 1
    return f"Renamed {count} files."


def archive_old(folder: str, days: int = 30) -> str:
    import shutil
    import time

    cutoff = time.time() - days * 86400
    archive = os.path.join(folder, "archived")
    os.makedirs(archive, exist_ok=True)
    moved = 0
    for f in os.listdir(folder):
        fp = os.path.join(folder, f)
        if os.path.isfile(fp) and os.path.getmtime(fp) < cutoff:
            shutil.move(fp, os.path.join(archive, f))
            moved += 1
    return f"Archived {moved} files older than {days} days."


def analyze_structure(folder: str) -> str:
    sizes = {}
    for root, dirs, files in os.walk(folder):
        for f in files:
            ext = f.split(".")[-1] if "." in f else "no_ext"
            sizes[ext] = sizes.get(ext, 0) + 1
    return "Extensions: " + ", ".join(
        f"{k}: {v}" for k, v in sorted(sizes.items(), key=lambda x: -x[1])[:10]
    )
