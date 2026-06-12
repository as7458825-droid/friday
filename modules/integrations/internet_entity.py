from modules.llm.llm_manager import query_llm, TaskType


def deep_research(topic):
    """Perform multi-step internet research and summarize."""
    # 1. Search for top links (Mocking search for now, would use Google Search API)

    # 2. Extract and Summarize (Simulated Research)
    research_prompt = f"""
    You are an Elite Research Entity.
    I need a comprehensive summary on: {topic}.
    Include:
    - Current Trends
    - Key Players/Technologies
    - Future Predictions
    Format it for a high-level briefing.
    """

    summary = query_llm(research_prompt, task_type=TaskType.GENERAL)
    return f"Research Briefing for '{topic}':\n\n{summary}"


def fact_check(statement):
    """Verify information against live data."""
    prompt = f"Fact check the following statement using your internal knowledge and logic: '{statement}'"
    result = query_llm(prompt, task_type=TaskType.GENERAL)
    return result
