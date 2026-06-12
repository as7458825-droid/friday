from modules.multi_agent.agents import (
    AGENT_REGISTRY,
    CommandAgent,
    FileAgent,
    SystemAgent,
    WebSearchAgent,
)

AGENT_KEYWORDS = {
    WebSearchAgent: ["search", "find", "look up", "google", "browse", "lookup"],
    FileAgent: [
        "file",
        "save",
        "write",
        "read",
        "create",
        "list",
        "folder",
        "mkdir",
        "dir",
    ],
    SystemAgent: ["cpu", "memory", "ram", "disk", "system", "battery", "process"],
    CommandAgent: ["run", "execute", "terminal", "command", "shell"],
}


def is_complex(task: str) -> bool:
    task_lower = task.lower()
    return any(
        any(kw in task_lower for kw in keywords) for keywords in AGENT_KEYWORDS.values()
    )


class AgentCoordinator:
    def __init__(self, task: str):
        self.task = task
        self.subtasks = []

    def decompose(self) -> list[dict]:
        task_lower = self.task.lower()
        self.subtasks = []

        for agent_cls, keywords in AGENT_KEYWORDS.items():
            if any(kw in task_lower for kw in keywords):
                self.subtasks.append(
                    {
                        "agent": agent_cls(),
                        "description": self.task,
                        "agent_name": agent_cls.name,
                    }
                )

        if not self.subtasks:
            self.subtasks.append(
                {
                    "agent": None,
                    "description": self.task,
                    "agent_name": "llm",
                }
            )

        return self.subtasks

    def execute(self) -> str:
        results = []
        for step in self.decompose():
            agent = step["agent"]
            if agent is None:
                from modules.llm.openrouter_client import ask_llm

                response = ask_llm(self.task)
                results.append(response or "No response from LLM.")
            else:
                results.append(agent.run(step))
        return "\n".join(results)


def get_agent_status() -> str:
    lines = []
    for name, cls in AGENT_REGISTRY.items():
        lines.append(f"{name}: {cls.description}")
    return "\n".join(lines)
