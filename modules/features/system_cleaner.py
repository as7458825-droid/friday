import os
import shutil
import tempfile


def clean_temp_files() -> str:
    freed = 0
    count = 0
    temp_dirs = [
        tempfile.gettempdir(),
        os.environ.get("TMP", ""),
        os.environ.get("TEMP", ""),
        os.path.expandvars("%LOCALAPPDATA%\\Temp"),
    ]
    for d in set(filter(None, temp_dirs)):
        if not os.path.isdir(d):
            continue
        for root, dirs, files in os.walk(d):
            for f in files:
                try:
                    fpath = os.path.join(root, f)
                    size = os.path.getsize(fpath)
                    os.remove(fpath)
                    freed += size
                    count += 1
                except Exception:
                    pass
    mb = freed / (1024 * 1024)
    return f"Cleaned {count} temp files ({mb:.1f} MB freed)."


def clean_recycle_bin() -> str:
    try:
        import ctypes

        ctypes.windll.shell32.SHEmptyRecycleBinW(None, 0, 1)
        return "Recycle bin emptied."
    except Exception as e:
        return f"Could not empty recycle bin: {e}"


def clean_browser_cache() -> str:
    cache_paths = [
        os.path.expandvars("%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Cache"),
        os.path.expandvars(
            "%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Code Cache"
        ),
        os.path.expandvars(
            "%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Cache"
        ),
        os.path.expandvars("%APPDATA%\\Opera Software\\Opera Stable\\Cache"),
    ]
    freed = 0
    count = 0
    for path in cache_paths:
        if not os.path.isdir(path):
            continue
        try:
            size = sum(
                os.path.getsize(os.path.join(path, f))
                for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            )
            shutil.rmtree(path, ignore_errors=True)
            os.makedirs(path, exist_ok=True)
            freed += size
            count += 1
        except Exception:
            pass
    mb = freed / (1024 * 1024)
    return f"Cleared {count} browser caches ({mb:.1f} MB)."


def clean_all() -> str:
    results = []
    results.append(clean_temp_files())
    results.append(clean_browser_cache())
    results.append(clean_recycle_bin())
    return " | ".join(results)
