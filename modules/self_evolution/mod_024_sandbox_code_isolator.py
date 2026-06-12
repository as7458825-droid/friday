import subprocess
import sys
import tempfile
import textwrap


def run_in_sandbox(code: str, timeout: int = 5) -> str:
    restricted_globals = {
        "__builtins__": {
            "abs": abs,
            "bool": bool,
            "dict": dict,
            "enumerate": enumerate,
            "float": float,
            "int": int,
            "len": len,
            "list": list,
            "max": max,
            "min": min,
            "print": print,
            "range": range,
            "round": round,
            "str": str,
            "sum": sum,
            "tuple": tuple,
            "zip": zip,
            "True": True,
            "False": False,
            "None": None,
        }
    }

    try:
        compiled = compile(
            textwrap.dedent(code),
            "<sandbox>",
            "exec",
        )
        exec(compiled, restricted_globals)
        return "Sandbox execution completed."
    except Exception as e:
        return f"Sandbox error: {e}"


def run_in_subprocess(code: str, timeout: int = 5) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(textwrap.dedent(code))
        f.flush()
        try:
            result = subprocess.run(
                [sys.executable, f.name],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode == 0:
                return result.stdout or "No output."
            return f"Error: {result.stderr[:300]}"
        except subprocess.TimeoutExpired:
            return "Sandbox execution timed out."
        except Exception as e:
            return f"Sandbox failed: {e}"
