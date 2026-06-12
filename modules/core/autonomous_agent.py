import json
import os
import time
import threading
from datetime import datetime, timedelta

TASKS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "memory_db", "autonomous_tasks.json"
)


class AutonomousAgent:
    """Agent for long-running background tasks."""

    def __init__(self):
        self.tasks = self._load_tasks()
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def _load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        return []

    def _save_tasks(self):
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, description, interval_minutes, duration_days=7):
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "interval": interval_minutes,
            "expiry": (datetime.now() + timedelta(days=duration_days)).isoformat(),
            "last_run": None,
            "status": "active",
        }
        self.tasks.append(task)
        self._save_tasks()
        return f"Autonomous task '{description}' scheduled every {interval_minutes} minutes."

    def _monitor_loop(self):
        while self.running:
            now = datetime.now()
            for task in self.tasks:
                if task["status"] != "active":
                    continue

                # Check expiry
                if now > datetime.fromisoformat(task["expiry"]):
                    task["status"] = "expired"
                    continue

                # Check interval
                last_run = task["last_run"]
                if (
                    not last_run
                    or (now - datetime.fromisoformat(last_run)).total_seconds() / 60
                    >= task["interval"]
                ):
                    self._execute_task(task)
                    task["last_run"] = now.isoformat()

            self._save_tasks()
            time.sleep(60)  # Check every minute

    def _execute_task(self, task):
        print(f"[AUTONOMOUS AGENT] Executing: {task['description']}")
        # In a real scenario, this would route to the LLM or specific modules
        # For now, we log the execution
        pass


# Global Instance
global_agent = AutonomousAgent()
