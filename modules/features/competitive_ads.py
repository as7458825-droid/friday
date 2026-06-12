def extract_fb_ads(competitor: str) -> str:
    try:
        pass
    except Exception:
        return "requests/bs4 not available."
    url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=IN&q={competitor}"
    return f"Open FB Ad Library manually: {url}"


def extract_linkedin_ads(competitor: str) -> str:
    url = f"https://www.linkedin.com/ads/library/?country=IN&q={competitor}"
    return f"Open LinkedIn Ad Library: {url}"


def analyze_messaging(competitors_text: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Analyze these competitor ads and identify patterns in messaging:\n{competitors_text}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Analysis done."
    except Exception:
        return "LLM not available."
