import datetime
import os
import sqlite3

from jinja2 import Template

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated")

SQLITE_TABLE = Template("""CREATE TABLE IF NOT EXISTS {{ table_name }} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    {{ columns }}
);
""")

POSTGRES_TABLE = Template("""CREATE TABLE IF NOT EXISTS {{ table_name }} (
    id SERIAL PRIMARY KEY,
    {{ columns }}
);
""")


def _ensure_generated_dir():
    os.makedirs(GENERATED_DIR, exist_ok=True)


def generate_schema(description: str, dialect: str = "sqlite") -> str:
    _ensure_generated_dir()

    try:
        from modules.llm.openrouter_client import ask_llm

        prompt = (
            f"Generate {dialect} SQL schema only (no explanation). "
            f"Description: {description}"
        )
        sql = ask_llm(prompt)
        if sql and "CREATE TABLE" in sql.upper():
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"schema_{ts}.sql"
            fpath = os.path.join(GENERATED_DIR, fname)
            with open(fpath, "w") as f:
                f.write(sql)
            return f"Schema generated -> {fpath}"
    except Exception:
        pass

    # fallback template
    parts = description.lower().split()
    table = parts[-1] if parts else "item"
    if dialect == "postgresql":
        sql = POSTGRES_TABLE.render(
            table_name=table,
            columns="name TEXT NOT NULL,\n    created_at TIMESTAMP DEFAULT NOW()",
        )
    else:
        sql = SQLITE_TABLE.render(
            table_name=table,
            columns="name TEXT NOT NULL,\n    created_at TEXT DEFAULT CURRENT_TIMESTAMP",
        )
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"schema_{ts}.sql"
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w") as f:
        f.write(sql)
    return f"Template schema generated -> {fpath}"


def migrate_database(connection_url: str, schema_sql: str) -> str:
    if connection_url.startswith("sqlite"):
        db_path = connection_url.replace("sqlite:///", "")
        try:
            conn = sqlite3.connect(db_path)
            conn.executescript(schema_sql)
            conn.commit()
            conn.close()
            return f"Schema applied to {db_path}"
        except Exception as e:
            return f"Migration failed: {e}"
    else:
        return "Only SQLite migrations supported currently"
