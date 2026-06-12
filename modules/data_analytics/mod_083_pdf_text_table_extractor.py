import datetime
import os

import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def _ensure_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_tables_from_pdf(pdf_path: str) -> list[pd.DataFrame]:
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")

    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_tables = page.extract_tables()
            for j, table in enumerate(page_tables):
                if table:
                    header = table[0] if table else []
                    data = table[1:] if len(table) > 1 else []
                    df = pd.DataFrame(data, columns=header)
                    tables.append(df)

                    _ensure_output()
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    csv_path = os.path.join(
                        OUTPUT_DIR, f"table_p{i + 1}_t{j + 1}_{ts}.csv"
                    )
                    df.to_csv(csv_path, index=False)

    return tables


def extract_text_by_page(pdf_path: str) -> dict[int, str]:
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber not installed")

    pages = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages[i + 1] = text

    _ensure_output()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = os.path.join(OUTPUT_DIR, f"pdf_text_{ts}.txt")
    with open(txt_path, "w") as f:
        for page_num, text in pages.items():
            f.write(f"\n=== Page {page_num} ===\n{text}\n")

    return pages
