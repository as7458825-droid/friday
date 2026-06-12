def research(topic: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Write a short researched article about {topic} with key facts and citations.",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Research complete."
    except Exception:
        return "LLM not available."


def write_blog(topic: str, tone: str = "professional") -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Write a {tone} blog post about {topic}. Include an intro, body, and conclusion.",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Blog generated."
    except Exception:
        return "LLM not available."


def rewrite(text: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Rewrite this text to be more engaging and clear:\n{text}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or text
    except Exception:
        return text


def seo_optimize(text: str, keywords: str = "") -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        kw = f" using keywords: {keywords}" if keywords else ""
        result = query_llm(
            f"SEO optimize this content{kw}:\n{text}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or text
    except Exception:
        return text
