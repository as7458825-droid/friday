def find_icp(description: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Define the Ideal Customer Profile for: {description}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Analysis done."
    except Exception:
        return "LLM not available."


def find_companies(industry: str) -> str:
    return (
        f"Search manually on: https://www.linkedin.com/sales/search?industry={industry}"
    )


def find_contacts(company: str) -> str:
    return f"Search: https://www.linkedin.com/search/results/people/?keywords={company}"


def generate_outreach(company: str, product: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Write a short cold outreach email to {company} about {product}.",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Email generated."
    except Exception:
        return "LLM not available."
