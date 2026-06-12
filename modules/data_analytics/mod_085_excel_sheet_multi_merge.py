import datetime
import os

import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def _ensure_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def merge_excel_files(file_list: list[str], output_path: str = None) -> str:
    if output_path is None:
        _ensure_output()
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"merged_{ts}.xlsx")

    writer = pd.ExcelWriter(output_path, engine="openpyxl")

    for filepath in file_list:
        if not os.path.isfile(filepath):
            continue
        try:
            xls = pd.ExcelFile(filepath, engine="openpyxl")
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(filepath, sheet_name=sheet_name, engine="openpyxl")
                safe_name = (
                    f"{os.path.splitext(os.path.basename(filepath))[0]}_{sheet_name}"[
                        :31
                    ]
                )
                df.to_excel(writer, sheet_name=safe_name, index=False)
        except Exception:
            pass

    writer.close()
    return f"Merged {len(file_list)} files -> {output_path}"


def merge_sheets_same_file(input_path: str, output_sheet_name: str = "merged") -> str:
    if not os.path.isfile(input_path):
        return f"File not found: {input_path}"

    xls = pd.ExcelFile(input_path, engine="openpyxl")
    all_dfs = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(input_path, sheet_name=sheet, engine="openpyxl")
        all_dfs.append(df)

    merged = pd.concat(all_dfs, ignore_index=True)

    _ensure_output()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"sheets_merged_{ts}.xlsx")

    merged.to_excel(output_path, sheet_name=output_sheet_name, index=False)
    return f"Merged {len(all_dfs)} sheets -> {output_path}"
