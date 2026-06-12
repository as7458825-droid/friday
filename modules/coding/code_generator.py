import os
import re
from datetime import datetime


GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated_code")

EXTENSION_MAP = {
    "python": ".py",
    "py": ".py",
    "javascript": ".js",
    "js": ".js",
    "typescript": ".ts",
    "ts": ".ts",
    "react": ".jsx",
    "jsx": ".jsx",
    "html": ".html",
    "css": ".css",
    "go": ".go",
    "rust": ".rs",
    "rs": ".rs",
    "java": ".java",
    "kotlin": ".kt",
    "kt": ".kt",
    "swift": ".swift",
    "c": ".c",
    "cpp": ".cpp",
    "c++": ".cpp",
    "csharp": ".cs",
    "cs": ".cs",
    "ruby": ".rb",
    "rb": ".rb",
    "php": ".php",
    "sql": ".sql",
    "bash": ".sh",
    "sh": ".sh",
    "shell": ".sh",
    "yaml": ".yaml",
    "yml": ".yml",
    "json": ".json",
    "markdown": ".md",
    "md": ".md",
}

_last_generated_path: str | None = None


def _ensure_dir():
    os.makedirs(GENERATED_DIR, exist_ok=True)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _detect_language(command: str) -> str:
    for lang in [
        "python",
        "javascript",
        "typescript",
        "react",
        "rust",
        "go",
        "java",
        "kotlin",
        "swift",
        "c++",
        "cpp",
        "c#",
        "csharp",
        "ruby",
        "php",
        "html",
        "css",
        "bash",
        "shell",
        "sql",
        "yaml",
        "json",
        "markdown",
    ]:
        if lang in command.lower():
            return lang
    return "python"


def _extract_code(text: str) -> str:
    """Extract code from markdown code blocks, or return text as-is."""
    pattern = r"```(?:\w+)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return "\n\n".join(m.strip() for m in matches).strip()
    return text.strip()


def _save_code(code: str, language: str, prefix: str = "generated") -> str:
    _ensure_dir()
    ext = EXTENSION_MAP.get(language.lower(), ".txt")
    fname = f"{prefix}_{_timestamp()}{ext}"
    fpath = os.path.join(GENERATED_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)
    global _last_generated_path
    _last_generated_path = fpath
    return fpath


def get_last_generated_path() -> str | None:
    return _last_generated_path


def generate_code(prompt: str, language: str | None = None) -> str:
    if not language:
        language = _detect_language(prompt)

    system = (
        f"You are a world-class {language} developer. "
        f"Generate clean, production-ready {language} code for the given task. "
        "Return ONLY the code inside a single markdown code block. "
        "No explanations, no comments outside the block."
    )

    from modules.llm.llm_manager import query_llm, TaskType

    result = query_llm(
        f"Write {language} code to: {prompt}",
        task_type=TaskType.CODING,
        system_override=system,
        max_tokens=4096,
    )
    if not result:
        return "Failed to generate code. Check your LLM configuration."

    code = _extract_code(result)
    fpath = _save_code(code, language, "generated")
    short = code[:200].replace("\n", " ")
    return f"Code saved to {fpath}. Preview: {short}..."


def edit_code(existing_code: str | None, instruction: str) -> str:
    if not existing_code:
        return "No previous code to edit. Generate some code first."

    system = (
        "You are a code editing assistant. Given existing code and an edit "
        "instruction, return the COMPLETE modified code inside a markdown "
        "code block. Preserve the original language and style."
    )

    from modules.llm.llm_manager import query_llm, TaskType

    result = query_llm(
        f"Existing code:\n```\n{existing_code[:4000]}\n```\n\n"
        f"Edit instruction: {instruction}",
        task_type=TaskType.CODING,
        system_override=system,
        max_tokens=4096,
    )
    if not result:
        return "Failed to edit code."

    code = _extract_code(result)
    lang = _detect_language(existing_code[:100])
    fpath = _save_code(code, lang, "edited")
    short = code[:200].replace("\n", " ")
    return f"Edited code saved to {fpath}. Preview: {short}..."


def debug_code(code: str, error: str = "") -> str:
    system = (
        "You are a debugging expert. Analyze the given code and error message. "
        "Identify bugs and provide the FIXED complete code inside a markdown "
        "code block. Briefly explain what was wrong, then return the fixed code."
    )

    from modules.llm.llm_manager import query_llm, TaskType

    query = f"Code:\n```\n{code[:4000]}\n```\n"
    if error:
        query += f"Error message: {error}\n"
    query += "\nDebug and fix the code."

    result = query_llm(
        query,
        task_type=TaskType.CODING,
        system_override=system,
        max_tokens=4096,
    )
    if not result:
        return "Failed to debug code."

    code = _extract_code(result)
    lang = _detect_language(code[:100]) or "python"
    fpath = _save_code(code, lang, "debugged")
    short = code[:200].replace("\n", " ")
    return f"Debugged code saved to {fpath}. Preview: {short}..."


def write_tests(code: str) -> str:
    system = (
        "You are a testing expert. Given source code, generate comprehensive "
        "unit tests. Return ONLY the test code inside a markdown code block. "
        "Use pytest for Python, jest for JavaScript, etc."
    )

    from modules.llm.llm_manager import query_llm, TaskType

    result = query_llm(
        f"Generate unit tests for this code:\n```\n{code[:4000]}\n```",
        task_type=TaskType.CODING,
        system_override=system,
        max_tokens=4096,
    )
    if not result:
        return "Failed to generate tests."

    tests = _extract_code(result)
    lang = (
        "python"
        if "def test_" in tests or "import pytest" in tests
        else _detect_language(tests[:100])
    )
    fpath = _save_code(tests, lang, "tests")
    short = tests[:200].replace("\n", " ")
    return f"Tests saved to {fpath}. Preview: {short}..."


def explain_code(code: str) -> str:
    system = (
        "You are a code explainer. Explain the given code in simple, "
        "natural language. Describe what it does, key functions, "
        "inputs/outputs, and any important patterns. Keep it concise."
    )

    from modules.llm.llm_manager import query_llm, TaskType

    result = query_llm(
        f"Explain this code:\n```\n{code[:6000]}\n```",
        task_type=TaskType.GENERAL,
        system_override=system,
        max_tokens=1024,
    )
    return result or "Failed to explain code."


def run_code_and_fix(code_path: str, max_iterations: int = 3) -> str:
    """Run code, catch errors, and attempt self-fixing up to max_iterations."""
    import subprocess

    current_path = code_path
    for i in range(max_iterations):
        result = subprocess.run(
            ["python", current_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            return f"Success on iteration {i + 1}!\nOutput: {result.stdout}"

        # If failed, debug and fix
        error_msg = result.stderr
        with open(current_path, "r") as f:
            code = f.read()

        print(f"Iteration {i + 1} failed. Attempting self-fix...")
        debug_res = debug_code(code, error_msg)
        # Extract path from debug_res
        match = re.search(r"saved to (.*?)\.", debug_res)
        if match:
            current_path = match.group(1).strip()
        else:
            return f"Fixing failed: {debug_res}"

    return f"Failed after {max_iterations} attempts. Last error: {result.stderr}"


def run_agentic_test(code_path: str) -> str:
    """Generate tests, run them, and fix code if tests fail."""
    import subprocess

    with open(code_path, "r") as f:
        code = f.read()

    # 1. Generate Tests
    test_res = write_tests(code)
    match = re.search(r"saved to (.*?)\.", test_res)
    if not match:
        return f"Test generation failed: {test_res}"
    test_path = match.group(1).strip()

    # 2. Run Tests
    for i in range(3):
        result = subprocess.run(
            ["pytest", test_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            return f"Tests passed successfully!\n{result.stdout}"

        print(f"Tests failed (Iteration {i + 1}). Fixing code...")
        # Debug the original code using test failure
        debug_res = debug_code(code, result.stdout)
        match = re.search(r"saved to (.*?)\.", debug_res)
        if match:
            code_path = match.group(1).strip()
            with open(code_path, "r") as f:
                code = f.read()
        else:
            return f"Self-fix failed: {debug_res}"

    return "Failed to fix code after 3 test-driven iterations."
