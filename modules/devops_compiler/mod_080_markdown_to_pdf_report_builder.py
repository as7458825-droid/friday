import os
import subprocess


def convert_markdown_to_pdf(md_file: str, output_pdf: str = None) -> str:
    if not os.path.isfile(md_file):
        return f"File not found: {md_file}"

    if output_pdf is None:
        output_pdf = os.path.splitext(md_file)[0] + ".pd"

    try:
        # Try weasyprint first
        import weasyprint
        import markdown

        with open(md_file) as f:
            md_text = f.read()

        html_body = markdown.markdown(
            md_text, extensions=["extra", "tables", "fenced_code"]
        )
        html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; line-height: 1.6; }}
h1 {{ color: #00d4ff; border-bottom: 2px solid #00d4ff; }}
h2 {{ color: #0a84ff; }}
code {{ background: #1a1a2e; color: #00ff88; padding: 2px 6px; border-radius: 3px; }}
pre {{ background: #1a1a2e; padding: 16px; border-radius: 6px; overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
th {{ background: #0a84ff; color: white; }}
blockquote {{ border-left: 4px solid #00d4ff; margin-left: 0; padding-left: 16px; color: #888; }}
</style></head>
<body>{html_body}</body></html>
"""

        weasyprint.HTML(string=html).write_pdf(output_pdf)
        return f"PDF generated -> {output_pdf}"

    except ImportError:
        pass

    try:
        # Fallback: try pdfkit
        import pdfkit
        import markdown

        with open(md_file) as f:
            md_text = f.read()

        html_body = markdown.markdown(
            md_text, extensions=["extra", "tables", "fenced_code"]
        )
        html = f"<html><body>{html_body}</body></html>"
        pdfkit.from_string(html, output_pdf)
        return f"PDF generated (pdfkit) -> {output_pdf}"

    except ImportError:
        pass

    # Last fallback: try pandoc
    try:
        subprocess.run(
            ["pandoc", md_file, "-o", output_pdf],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return f"PDF generated (pandoc) -> {output_pdf}"
    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
    ):
        return "No PDF renderer available. Install weasyprint or pandoc."
