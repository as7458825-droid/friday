def generate_ideas(description: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Generate 10 creative domain name ideas for: {description}. Just list them.",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "LLM not available."
    except Exception:
        return "LLM not available."


def check_availability(domain: str) -> str:
    try:
        import requests
    except Exception:
        return f"Check manually: https://www.namecheap.com/domains/registration/results/?domain={domain}"
    try:
        r = requests.get(f"https://rdap.verisign.com/com/v1/domain/{domain}", timeout=5)
        if r.status_code == 200:
            return f"{domain} is TAKEN"
        return f"{domain} may be AVAILABLE"
    except Exception:
        return f"Check: https://www.namecheap.com/domains/registration/results/?domain={domain}"


def find_expiring() -> str:
    return "Visit: https://www.expireddomains.net/ or https://namecheap.com"
