def analyze_code(repo_path: str = ".") -> str:
    try:
        import subprocess

        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--oneline", "-30"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return f"Recent commits:\n{result.stdout or 'No git history'}"
    except Exception:
        return "Git not available."


def find_gaps(language: str = "python") -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"List the top 5 skills a {language} developer should learn in 2026 to stay relevant.",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Analysis done."
    except Exception:
        return "LLM not available."


def get_learning_plan(goal: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Create a 4-week learning plan to achieve: {goal}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Plan generated."
    except Exception:
        return "LLM not available."
