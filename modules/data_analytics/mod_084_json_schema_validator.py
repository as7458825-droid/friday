import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def validate_json(json_data: dict | str, schema: dict | str) -> dict:
    try:
        import jsonschema
    except ImportError:
        raise ImportError("jsonschema not installed. Run: pip install jsonschema")

    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    if isinstance(schema, str):
        schema = json.loads(schema)

    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(json_data):
        errors.append(
            {
                "path": list(error.absolute_path),
                "message": error.message,
                "schema_path": list(error.schema_path),
            }
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "error_count": len(errors),
    }


def infer_schema_from_json(json_data: dict | str) -> dict:
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    def _infer_type(value):
        if isinstance(value, bool):
            return {"type": "boolean"}
        if isinstance(value, int):
            return {"type": "integer"}
        if isinstance(value, float):
            return {"type": "number"}
        if isinstance(value, str):
            return {"type": "string"}
        if isinstance(value, list):
            if value:
                items = _infer_type(value[0])
                return {"type": "array", "items": items}
            return {"type": "array"}
        if isinstance(value, dict):
            return {
                "type": "object",
                "properties": {k: _infer_type(v) for k, v in value.items()},
            }
        return {"type": "null"}

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "required": [],
    }
    for key, value in json_data.items():
        schema["properties"][key] = _infer_type(value)
        schema["required"].append(key)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fpath = os.path.join(OUTPUT_DIR, "inferred_schema.json")
    with open(fpath, "w") as f:
        json.dump(schema, f, indent=2)

    return schema
