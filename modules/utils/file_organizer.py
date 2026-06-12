import os
import shutil
from datetime import datetime

EXTENSION_MAP = {
    "images": [".jpg", ".jpeg", ".png", ".gi", ".bmp", ".tif", ".webp", ".svg"],
    "documents": [".pd", ".doc", ".docx", ".txt", ".rt", ".odt", ".md"],
    "spreadsheets": [".xls", ".xlsx", ".csv", ".tsv", ".ods"],
    "presentations": [".ppt", ".pptx", ".odp"],
    "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
    "video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "code": [
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".html",
        ".css",
        ".scss",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".go",
        ".rs",
        ".rb",
        ".php",
        ".swift",
        ".kt",
        ".dart",
        ".sql",
        ".sh",
        ".bat",
        ".ps1",
    ],
    "executables": [".exe", ".msi", ".app", ".deb", ".rpm"],
}

ORGANIZED_LOG = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "organizer_log.json"
)


def analyze_folder(path: str) -> str:
    if not os.path.isdir(path):
        return f"Folder not found: {path}"
    counts = {}
    total = 0
    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1].lower()
            matched = False
            for category, exts in EXTENSION_MAP.items():
                if ext in exts:
                    counts[category] = counts.get(category, 0) + 1
                    matched = True
                    break
            if not matched:
                counts["other"] = counts.get("other", 0) + 1
            total += 1
    if total == 0:
        return f"Folder '{path}' is empty."
    lines = [f"Folder: {path} ({total} files)"]
    for cat, count in sorted(counts.items()):
        lines.append(f"  {cat}: {count}")
    return "\n".join(lines)


def organize_folder(path: str, dry_run: bool = True) -> str:
    if not os.path.isdir(path):
        return f"Folder not found: {path}"
    moved = 0
    errors = 0
    log_entries = []
    for fname in os.listdir(path):
        fpath = os.path.join(path, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1].lower()
            target_dir = None
            for category, exts in EXTENSION_MAP.items():
                if ext in exts:
                    target_dir = os.path.join(path, category)
                    break
            if target_dir is None:
                target_dir = os.path.join(path, "other")
            if dry_run:
                moved += 1
                log_entries.append(f"Would move: {fname} -> {target_dir}")
            else:
                os.makedirs(target_dir, exist_ok=True)
                try:
                    dest = os.path.join(target_dir, fname)
                    if os.path.isfile(dest):
                        base, ext = os.path.splitext(fname)
                        dest = os.path.join(
                            target_dir,
                            f"{base}_{datetime.now().strftime('%H%M%S')}{ext}",
                        )
                    shutil.move(fpath, dest)
                    moved += 1
                    log_entries.append(f"Moved: {fname} -> {target_dir}")
                except Exception:
                    errors += 1
    import json

    mem_dir = os.path.dirname(ORGANIZED_LOG)
    if not os.path.isdir(mem_dir):
        os.makedirs(mem_dir, exist_ok=True)
    existing = []
    if os.path.isfile(ORGANIZED_LOG):
        with open(ORGANIZED_LOG) as f:
            existing = json.load(f)
    existing.append(
        {
            "path": path,
            "moved": moved,
            "errors": errors,
            "dry_run": dry_run,
            "time": datetime.now().isoformat(),
        }
    )
    with open(ORGANIZED_LOG, "w") as f:
        json.dump(existing, f, indent=2)
    action = "Would move" if dry_run else "Moved"
    msg = f"{action} {moved} files"
    if errors:
        msg += f" ({errors} errors)"
    if dry_run:
        msg += ". Say 'organize {path}' to execute."
    return msg


def find_duplicates(path: str) -> str:
    if not os.path.isdir(path):
        return f"Folder not found: {path}"
    import hashlib

    hashes = {}
    for root, dirs, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "rb") as f:
                    file_hash = hashlib.md5(f.read(65536)).hexdigest()
                if file_hash in hashes:
                    hashes[file_hash].append(fpath)
                else:
                    hashes[file_hash] = [fpath]
            except Exception:
                pass
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    if not duplicates:
        return "No duplicate files found."
    lines = []
    for h, paths in duplicates.items():
        lines.append(f"Duplicate ({len(paths)} copies):")
        for p in paths:
            lines.append(f"  {p}")
    return "\n".join(lines[:20])
