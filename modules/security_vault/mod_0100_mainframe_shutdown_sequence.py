import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "audit_log.db"
)


def _get_db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS audit ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "timestamp TEXT, event TEXT, details TEXT)"
    )
    return conn


def log_event(event: str, details: str = ""):
    conn = _get_db()
    conn.execute(
        "INSERT INTO audit (timestamp, event, details) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), event, details),
    )
    conn.commit()
    conn.close()


def view_log(limit: int = 20) -> list[dict]:
    conn = _get_db()
    rows = conn.execute(
        "SELECT timestamp, event, details FROM audit ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [{"timestamp": r[0], "event": r[1], "details": r[2]} for r in rows]
