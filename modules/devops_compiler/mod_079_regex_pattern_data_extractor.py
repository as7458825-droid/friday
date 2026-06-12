import datetime
import json
import os
import re

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated")


PREDEFINED_PATTERNS = {
    "email": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
    "url": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[\w./?%&=-]*)?",
    "phone": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "ipv4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "hashtag": r"#\w+",
    "mention": r"@\w+",
}


def extract_patterns(
    text: str,
    pattern_type: str = "email",
    custom_pattern: str = None,
) -> dict:
    if custom_pattern:
        pattern = re.compile(custom_pattern)
    elif pattern_type in PREDEFINED_PATTERNS:
        pattern = re.compile(PREDEFINED_PATTERNS[pattern_type])
    else:
        return {
            "error": f"Unknown pattern type: {pattern_type}. Available: {list(PREDEFINED_PATTERNS.keys())}"
        }

    matches = pattern.findall(text)
    unique = list(set(matches))

    return {
        "pattern_type": pattern_type,
        "total_matches": len(matches),
        "unique_matches": len(unique),
        "matches": unique[:20],
    }


def extract_from_file(file_path: str, pattern_type: str = "email") -> dict:
    if not os.path.isfile(file_path):
        return {"error": f"File not found: {file_path}"}
    with open(file_path, errors="ignore") as f:
        text = f.read()
    result = extract_patterns(text, pattern_type)
    result["source_file"] = file_path

    fname = f"extracted_{pattern_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs(GENERATED_DIR, exist_ok=True)
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w") as f:
        json.dump(result, f, indent=2)

    result["saved_to"] = fpath
    return result
