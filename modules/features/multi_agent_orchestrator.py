import time
import threading
from datetime import datetime

_agents = {}
_results = {}


def create(name: str, task: str) -> str:
    _agents[name] = {
        "task": task,
        "status": "pending",
        "created": datetime.now().isoformat(),
    }
    return f"Agent '{name}' created with task: {task}"


def run(name: str) -> str:
    if name not in _agents:
        return f"Agent '{name}' not found."
    _agents[name]["status"] = "running"

    def _execute():
        try:
            from advanced.llm.llm_manager import query_llm, TaskType

            task = _agents[name]["task"]
            result = query_llm(
                f"You are agent '{name}'. Complete this task: {task}",
                task_type=TaskType.FAST_CONVERSATION,
            )
            _results[name] = result or "Task completed."
            _agents[name]["status"] = "completed"
        except Exception:
            _agents[name]["status"] = "failed"
            _results[name] = "LLM error."

    threading.Thread(target=_execute, daemon=True).start()
    return f"Agent '{name}' is running in background."


def run_all() -> str:
    count = 0
    for name in list(_agents.keys()):
        if _agents[name]["status"] == "pending":
            run(name)
            count += 1
    return f"Started {count} agents."


def status(name: str = "") -> str:
    if name:
        a = _agents.get(name)
        return f"{name}: {a['status']} - {a['task'][:50]}" if a else "Not found."
    if not _agents:
        return "No agents created."
    return " | ".join(f"{n}: {a['status']}" for n, a in _agents.items())


def result(name: str) -> str:
    res = _results.get(name, "No result yet.")
    return f"Result for '{name}': {res[:200]}"


def schedule(name: str, interval_hours: int) -> str:
    def _scheduled():
        while True:
            run(name)
            time.sleep(interval_hours * 3600)

    threading.Thread(target=_scheduled, daemon=True).start()
    return f"Agent '{name}' scheduled every {interval_hours}h"
