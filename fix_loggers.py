import os
import re


def fix_missing_loggers():
    dirs_to_scan = ["core", "modules"]
    fixed_count = 0

    for d in dirs_to_scan:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Check if 'logger.' is used
                    if re.search(r"\blogger\.", content):
                        # Check if logger is defined or imported
                        is_defined = re.search(r"logger\s*=", content)
                        is_imported = re.search(r"(import|from).*\blogger\b", content)

                        if not is_defined and not is_imported:
                            lines = content.split("\n")

                            has_logging_import = re.search(
                                r"^\s*import logging\b", content, re.MULTILINE
                            )

                            new_lines = []
                            if not has_logging_import:
                                new_lines.append("import logging")
                            new_lines.append("logger = logging.getLogger(__name__)")
                            new_lines.append("")

                            # Insert after __future__ imports if they exist
                            insert_idx = 0
                            for i, line in enumerate(lines):
                                if line.strip().startswith("from __future__"):
                                    insert_idx = i + 1

                            # Inject new lines
                            for i, new_line in enumerate(new_lines):
                                lines.insert(insert_idx + i, new_line)

                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write("\n".join(lines))

                            fixed_count += 1
                            print(f"Fixed missing logger in: {filepath}")

    print(f"\nTotal files fixed: {fixed_count}")


if __name__ == "__main__":
    fix_missing_loggers()
