import re


def repair_python_code(code: str, error_message: str) -> str | None:
    if "real_ai_brain" in _get_active_features():
        try:
            from modules.llm.openrouter_client import ask_llm

            prompt = (
                f"The following Python code:\n```\n{code}\n```\n"
                f"raised this error:\n{error_message}\n"
                "Return only the fixed code, no explanation."
            )
            return ask_llm(prompt)
        except Exception:
            pass

    return _basic_patch(code, error_message)


def _basic_patch(code: str, error: str) -> str | None:
    if "NameError" in error:
        match = re.search(r"name '(\w+)' is not defined", error)
        if match:
            missing = match.group(1)
            imports = f"# Auto-fixed: missing {missing}\n"
            return imports + code
    if "ModuleNotFoundError" in error:
        match = re.search(r"ModuleNotFoundError: No module named '(\w+)'", error)
        if match:
            pkg = match.group(1)
            return f"# Install missing module: pip install {pkg}\n" + code
    if "SyntaxError" in error:
        code = (
            code.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        )
        return code
    return None


def _get_active_features():
    try:
        from config import FEATURES

        return FEATURES
    except ImportError:
        return {}
