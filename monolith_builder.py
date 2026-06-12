import os
import re


def build_monolith():
    print("Rebuilding monolith with SIMPLE-APPEND method...")
    output_file = "main.py"

    external_imports = set()
    combined_body = []

    internal_names = [
        "modules",
        "core",
        "config",
        "startup_cache",
        "performance_profiler",
        "main",
        "advanced",
        "data",
    ]

    def is_internal_import(line):
        line = line.strip()
        if not (line.startswith("import ") or line.startswith("from ")):
            return False
        for name in internal_names:
            if re.search(r"\b" + name + r"\b", line):
                return True
        return False

    def process_file(file_path):
        print(f"Processing: {file_path}")
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        file_body = []
        in_main_block = False
        in_multiline_import = False

        for line in lines:
            stripped = line.strip()

            # Skip entry points
            if stripped.startswith('if __name__ == "__main__":') or stripped.startswith(
                "if __name__ == '__main__':"
            ):
                in_main_block = True
                continue
            if in_main_block:
                if stripped and not line.startswith(" ") and not line.startswith("\t"):
                    in_main_block = False
                else:
                    continue

            # Strip out repeated logger definitions to prevent IDE warnings
            if (
                "logger = logging.getLogger" in stripped
                or "log = logging.getLogger" in stripped
            ):
                continue

            # Strip internal imports
            if in_multiline_import:
                if ")" in line:
                    in_multiline_import = False
                continue

            if stripped.startswith("import ") or stripped.startswith("from "):
                if is_internal_import(line):
                    if "(" in line and ")" not in line:
                        in_multiline_import = True

                    # Add pass if the next non-empty line starts with except/finally/else
                    # This prevents IndentationError
                    file_body.append(re.match(r"^(\s*)", line).group(1) + "pass\n")
                    continue
                else:
                    indentation = re.match(r"^(\s*)", line).group(1)
                    if not indentation:
                        # Global import: extract to top, don't append to body
                        external_imports.add(stripped)
                        if "(" in line and ")" not in line:
                            pass
                        continue
                    else:
                        # Indented import (lazy/optional): leave it where it is
                        file_body.append(line)
                        if "(" in line and ")" not in line:
                            in_multiline_import = True
                        continue

            # Fix paths
            line = re.sub(r"(['\"])advanced/", r"\1modules/", line)
            line = re.sub(r"(['\"])advanced\.", r"\1modules.", line)
            line = re.sub(
                r"(['\"])(chroma_data|memory_db|output|generated)/", r"\1data/\2/", line
            )
            line = re.sub(
                r"(['\"])(chroma_data|memory_db|output|generated)(['\"])",
                r"\1data/\2\3",
                line,
            )

            file_body.append(line)

        return "".join(file_body)

    target_files = ["config.py", "startup_cache.py", "performance_profiler.py"]
    for d in ["core", "modules"]:
        for root, _, files in sorted(os.walk(d)):
            for file in sorted(files):
                if file.endswith(".py") and "__init__.py" not in file:
                    target_files.append(os.path.join(root, file))

    # We don't process main_backup or main.py to avoid loops

    for f_path in target_files:
        if os.path.exists(f_path):
            code = process_file(f_path)
            if code.strip():
                combined_body.append(
                    f"\n# {'=' * 40}\n# FILE: {f_path}\n# {'=' * 40}\n" + code
                )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# ruff: noqa\n")
        f.write("from __future__ import annotations\n")
        f.write(
            "import os, sys, time, logging, threading, json, random, re, math, subprocess, datetime, base64, io, socket, queue, importlib, inspect\n"
        )
        f.write("from datetime import datetime, date, timedelta\n")

        # Collect all unique external imports
        final_imps = sorted(list(external_imports))
        for imp in final_imps:
            if not is_internal_import(imp) and "__future__" not in imp:
                f.write("try:\n")
                f.write(f"    {imp}\n")
                f.write("except ImportError:\n")
                f.write("    pass\n")

        # Add single global logger
        f.write("\n# Global Logger\n")
        f.write(
            "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')\n"
        )
        f.write("log = logging.getLogger('FRIDAY')\n")
        f.write("logger = log\n")

        f.write("\n" + "".join(combined_body))

        f.write(
            "\n\nif __name__ == '__main__':\n    try:\n        # Fix for empty try blocks if any leaked\n        pass\n        ui_class = globals().get('AnimeAssistant') or globals().get('NovaOrb')\n        if ui_class:\n            app = ui_class()\n            app.run()\n        else:\n            if 'main' in globals(): globals()['main']()\n            else: print('System Error: main() not found.')\n    except Exception as e: print(f'Startup Error: {e}')\n"
        )

    print(f"Simple monolith built: {output_file}")


if __name__ == "__main__":
    build_monolith()
