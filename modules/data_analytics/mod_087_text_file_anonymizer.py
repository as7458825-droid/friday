import datetime
import os
import re

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")

PATTERNS = {
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "PHONE": re.compile(
        r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    ),
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "AADHAAR": re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
    "PAN": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
    "IP": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
}


def anonymize_text(text: str, entities: list[str] = None) -> str:
    if entities is None:
        entities = ["EMAIL", "PHONE"]

    for entity in entities:
        if entity in PATTERNS:
            text = PATTERNS[entity].sub(f"[{entity}:REDACTED]", text)

    # fallback for PERSON names (capitalized words after common titles)
    if "PERSON" in entities:
        title_pattern = re.compile(
            r"\b(?:Mr|Mrs|Ms|Dr|Prof|Shri|Smt)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*"
        )
        text = title_pattern.sub("[PERSON:REDACTED]", text)

    return text


def anonymize_file(file_path: str, entities: list[str] = None) -> str:
    if not os.path.isfile(file_path):
        return f"File not found: {file_path}"

    with open(file_path, errors="ignore") as f:
        content = f.read()

    anonymized = anonymize_text(content, entities)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"anonymized_{os.path.basename(file_path)}"
    fpath = os.path.join(OUTPUT_DIR, fname)
    with open(fpath, "w") as f:
        f.write(anonymized)

    return f"Anonymized file -> {fpath}"
