import os
import platform
import subprocess

import psutil
import requests

AGENT_REGISTRY = {}


def register(cls):
    AGENT_REGISTRY[cls.__name__] = cls
    return cls


@register
class WebSearchAgent:
    name = "WebSearchAgent"
    description = "Searches the web via DuckDuckGo API"

    def run(self, task: dict) -> str:
        query = task.get("query") or task.get("description", "")
        try:
            resp = requests.get(
                "https://api.duckduckgo.com",
                params={"q": query, "format": "json", "no_html": 1},
                timeout=10,
            )
            data = resp.json()
            answer = data.get("AbstractText") or data.get("Answer")
            return answer or f'Searched for "{query}" — no summary found.'
        except Exception as e:
            return f"Web search failed: {e}"


@register
class FileAgent:
    name = "FileAgent"
    description = "Reads, writes, creates files and lists directories"

    def run(self, task: dict) -> str:
        instruction = task.get("description", "")
        parts = instruction.lower().split()
        try:
            if "write" in parts or "create" in parts or "save" in parts:
                filename = task.get("filename", "output.txt")
                content = task.get("content", instruction)
                with open(filename, "w") as f:
                    f.write(content)
                return f"Written to {filename}"

            if "read" in parts or "open" in parts:
                filename = task.get("filename", "")
                if not filename:
                    for word in parts:
                        if os.path.isfile(word):
                            filename = word
                            break
                if filename and os.path.isfile(filename):
                    with open(filename) as f:
                        return f.read()[:500]
                return "File not found."

            if "mkdir" in parts or "create folder" in instruction.lower():
                dirname = task.get("dirname", "new_folder")
                os.makedirs(dirname, exist_ok=True)
                return f"Created folder {dirname}"

            if "list" in parts or "dir" in parts:
                target = task.get("path", ".")
                entries = os.listdir(target)
                return f"{len(entries)} items: {', '.join(entries[:20])}"

            return "FileAgent: instruction not recognized."
        except Exception as e:
            return f"File operation failed: {e}"


@register
class SystemAgent:
    name = "SystemAgent"
    description = "Reports CPU, memory, disk, battery, OS and process info"

    def run(self, task: dict) -> str:
        instruction = task.get("description", "").lower()
        if "cpu" in instruction:
            return f"CPU usage is {psutil.cpu_percent()}%."
        if "memory" in instruction or "ram" in instruction:
            mem = psutil.virtual_memory()
            return f"Memory: {mem.percent}% used ({mem.used // 1024**3} GB / {mem.total // 1024**3} GB)."
        if "disk" in instruction:
            disk = psutil.disk_usage("/")
            return f"Disk: {disk.percent}% used ({disk.free // 1024**3} GB free)."
        if "os" in instruction or "system" in instruction:
            return f"Running {platform.system()} {platform.release()}."
        if "battery" in instruction:
            bat = psutil.sensors_battery()
            if bat:
                return f"Battery at {bat.percent}%, {'plugged in' if bat.power_plugged else 'on battery'}."
            return "No battery detected."
        if "process" in instruction:
            return f"{len(psutil.pids())} processes running."
        return f"System info: {platform.platform()}, {psutil.cpu_count()} CPUs."


@register
class CommandAgent:
    name = "CommandAgent"
    description = "Runs system commands with user confirmation"

    def run(self, task: dict) -> str:
        cmd = task.get("command", task.get("description", ""))
        print(f"\n[SECURITY] CommandAgent wants to run: {cmd}")
        confirm = input("Allow this command? (yes/no): ").strip().lower()
        if confirm != "yes":
            return "Command cancelled by user."
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout or result.stderr
            return output[:500] or "Command executed (no output)."
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except Exception as e:
            return f"Command failed: {e}"
