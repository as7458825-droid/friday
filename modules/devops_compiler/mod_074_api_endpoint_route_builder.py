import datetime
import os

from jinja2 import Template

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated")

FASTAPI_CRUD_TEMPLATE = Template("""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class {{ resource }}Base(BaseModel):
    {% for field in fields %}
    {{ field.name }}: {{ field.type }}
    {% endfor %}

class {{ resource }}Create({{ resource }}Base):
    pass

class {{ resource }}({{ resource }}Base):
    id: int

_db: List[dict] = []
_counter = 0

@app.post("/{{ endpoint }}", response_model={{ resource }})
def create_item(item: {{ resource }}Create):
    global _counter
    _counter += 1
    entry = item.dict()
    entry["id"] = _counter
    _db.append(entry)
    return entry

@app.get("/{{ endpoint }}", response_model=List[{{ resource }}])
def list_items():
    return _db

@app.get("/{{ endpoint }}/{item_id}", response_model={{ resource }})
def get_item(item_id: int):
    for item in _db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Not found")

@app.put("/{{ endpoint }}/{item_id}", response_model={{ resource }})
def update_item(item_id: int, item: {{ resource }}Create):
    for i, existing in enumerate(_db):
        if existing["id"] == item_id:
            _db[i] = item.dict()
            _db[i]["id"] = item_id
            return _db[i]
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/{{ endpoint }}/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(_db):
        if item["id"] == item_id:
            del _db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Not found")
""")


def create_rest_api(resource_name: str, fields: list[dict] | None = None) -> str:
    os.makedirs(GENERATED_DIR, exist_ok=True)

    if fields is None:
        fields = [
            {"name": "name", "type": "str"},
            {"name": "description", "type": "Optional[str] = None"},
        ]

    try:
        from modules.llm.openrouter_client import ask_llm

        fields_desc = ", ".join(f"{f['name']}: {f['type']}" for f in fields)
        prompt = (
            f"Generate a FastAPI CRUD API for resource '{resource_name}' "
            f"with fields: {fields_desc}. Return only Python code."
        )
        code = ask_llm(prompt)
        if code and "FastAPI" in code:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"api_{resource_name.lower()}_{ts}.py"
            fpath = os.path.join(GENERATED_DIR, fname)
            with open(fpath, "w") as f:
                f.write(code)
            return f"LLM-generated API -> {fpath}"
    except Exception:
        pass

    code = FASTAPI_CRUD_TEMPLATE.render(
        resource=resource_name,
        endpoint=resource_name.lower(),
        fields=fields,
    )
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"api_{resource_name.lower()}_{ts}.py"
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w") as f:
        f.write(code)
    return f"Template API generated -> {fpath}"
