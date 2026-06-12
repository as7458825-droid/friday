import ast
import datetime
import os

from jinja2 import Template

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated")

TEST_TEMPLATE = Template("""import pytest
{{ imports }}

{{ test_functions }}
""")


def _ensure_generated_dir():
    os.makedirs(GENERATED_DIR, exist_ok=True)


def _ts():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_tests(module_path: str) -> str:
    if not os.path.isfile(module_path):
        return f"File not found: {module_path}"

    module_name = os.path.splitext(os.path.basename(module_path))[0]

    try:
        from modules.llm.openrouter_client import ask_llm

        with open(module_path) as f:
            content = f.read()
        prompt = (
            "Generate pytest test cases for this Python module. "
            f"Return only Python code with proper imports.\n\n{content}"
        )
        tests = ask_llm(prompt)
        if tests and "def test_" in tests:
            _ensure_generated_dir()
            fname = f"test_{module_name}_{_ts()}.py"
            fpath = os.path.join(GENERATED_DIR, fname)
            with open(fpath, "w") as f:
                f.write(tests)
            return f"LLM-generated tests -> {fpath}"
    except Exception:
        pass

    # fallback: parse functions and create stub tests
    with open(module_path) as f:
        source = f.read()

    tree = ast.parse(source)
    funcs = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    ]

    imports = f"from {module_name} import " + ", ".join(f.name for f in funcs)
    tests = []
    for func in funcs:
        tests.append("""
def test_{func.name}():
    result = {func.name}()
    assert result is not None
""")

    code = TEST_TEMPLATE.render(imports=imports, test_functions="\n".join(tests))
    _ensure_generated_dir()
    fname = f"test_{module_name}_{_ts()}.py"
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w") as f:
        f.write(code)
    return f"Template tests ({len(funcs)} functions) -> {fpath}"
