import os

from PyPDF2 import PdfReader, PdfWriter


def merge_pdfs(input_paths: list, output_path: str = "") -> str:
    if not output_path:
        output_path = os.path.join(os.path.dirname(__file__), "..", "..", "merged.pd")
    try:
        writer = PdfWriter()
        for path in input_paths:
            if os.path.isfile(path):
                reader = PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)
            else:
                return f"File not found: {path}"
        with open(output_path, "wb") as f:
            writer.write(f)
        return f"Merged {len(input_paths)} PDFs into {output_path}"
    except Exception as e:
        return f"Merge error: {e}"


def split_pdf(input_path: str, page_range: str = "1") -> str:
    if not os.path.isfile(input_path):
        return f"File not found: {input_path}"
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        total = len(reader.pages)
        parts = page_range.split(",")
        for part in parts:
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                for i in range(int(start) - 1, int(end)):
                    if 0 <= i < total:
                        writer.add_page(reader.pages[i])
            else:
                i = int(part) - 1
                if 0 <= i < total:
                    writer.add_page(reader.pages[i])
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_split.pd"
        with open(output_path, "wb") as f:
            writer.write(f)
        return f"Split pages {page_range} to {output_path}"
    except Exception as e:
        return f"Split error: {e}"


def watermark_pdf(input_path: str, watermark_text: str) -> str:
    if not os.path.isfile(input_path):
        return f"File not found: {input_path}"
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io

        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        c.setFont("Helvetica", 30)
        c.setFillColorRGB(0.5, 0.5, 0.5, 0.3)
        c.saveState()
        c.translate(300, 400)
        c.rotate(45)
        c.drawString(0, 0, watermark_text)
        c.restoreState()
        c.save()
        packet.seek(0)
        watermark = PdfReader(packet)
        wm_page = watermark.pages[0]
        for page in reader.pages:
            page.merge_page(wm_page)
            writer.add_page(page)
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_watermarked.pd"
        with open(output_path, "wb") as f:
            writer.write(f)
        return f"Watermarked PDF saved to {output_path}"
    except Exception as e:
        return f"Watermark error: {e}"


def rotate_pdf(input_path: str, angle: int = 90) -> str:
    if not os.path.isfile(input_path):
        return f"File not found: {input_path}"
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for page in reader.pages:
            page.rotate(angle)
            writer.add_page(page)
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_rotated.pd"
        with open(output_path, "wb") as f:
            writer.write(f)
        return f"Rotated PDF by {angle} degrees -> {output_path}"
    except Exception as e:
        return f"Rotate error: {e}"


def extract_text_from_pdf(input_path: str) -> str:
    if not os.path.isfile(input_path):
        return f"File not found: {input_path}"
    try:
        reader = PdfReader(input_path)
        texts = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text()
            if t:
                texts.append(f"[Page {i + 1}]: {t.strip()}")
        if texts:
            return "\n".join(texts)[:2000]
        return "No text extracted from PDF."
    except Exception as e:
        return f"Extract error: {e}"
