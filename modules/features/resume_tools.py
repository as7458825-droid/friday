import os

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "resumes.json"
)


def tailor(jd_text: str, resume_text: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Tailor this resume for this job description. Keep it concise:\n\nJD:\n{jd_text}\n\nResume:\n{resume_text}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Resume tailored."
    except Exception:
        return "LLM not available."


def cover_letter(jd_text: str, name: str = "") -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Write a professional cover letter for this job description. Name: {name or 'Applicant'}\n\n{jd_text}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Cover letter generated."
    except Exception:
        return "LLM not available."


def ats_score(resume_text: str, jd_text: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Score this resume against the JD from 0-100 for ATS compatibility. Give score and brief reason:\n\nResume:\n{resume_text[:1000]}\n\nJD:\n{jd_text[:1000]}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Score unavailable."
    except Exception:
        return "LLM not available."
