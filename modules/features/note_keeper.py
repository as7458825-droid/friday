import json
import os
from datetime import datetime

NOTES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "notes.json"
)


def _load():
    if os.path.isfile(NOTES_FILE):
        with open(NOTES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def _save(notes):
    mem = os.path.dirname(NOTES_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def add_note(text: str, category: str = "general") -> str:
    notes = _load()
    notes.append(
        {
            "id": len(notes) + 1,
            "text": text,
            "category": category,
            "created": datetime.now().isoformat(),
        }
    )
    _save(notes)
    return f"Note saved in {category}."


def list_notes(category: str = "") -> str:
    notes = _load()
    if category:
        notes = [n for n in notes if n["category"] == category]
    if not notes:
        return "No notes found."
    lines = [f"{n['id']}. {n['text'][:80]}" for n in notes[-10:]]
    return "Notes: " + " | ".join(lines)


def search_notes(query: str) -> str:
    notes = _load()
    results = [n for n in notes if query.lower() in n["text"].lower()]
    if not results:
        return f"No notes matching '{query}'."
    return "Found: " + " | ".join(n["text"][:80] for n in results[-5:])


def delete_note(note_id: int) -> str:
    notes = _load()
    for i, n in enumerate(notes):
        if n["id"] == note_id:
            notes.pop(i)
            _save(notes)
            return f"Note {note_id} deleted."
    return f"Note {note_id} not found."


def get_note_count() -> str:
    notes = _load()
    cats = {}
    for n in notes:
        cats[n["category"]] = cats.get(n["category"], 0) + 1
    return f"Total {len(notes)} notes. " + ", ".join(
        f"{c}: {v}" for c, v in cats.items()
    )
