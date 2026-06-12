import git
import docker
import logging

logger = logging.getLogger(__name__)


class DevOpsEngine:
    """Advanced Coding & DevOps Deployment Engine"""

    def commit_and_push(self, repo_path=".", commit_msg="Automated commit by FRIDAY"):
        """Commits changes to the current git repository"""
        try:
            repo = git.Repo(repo_path)
            repo.git.add(update=True)
            repo.index.commit(commit_msg)
            # repo.remotes.origin.push() # Commented out for safety
            return f"Git Module: Committed changes with message '{commit_msg}'."
        except Exception as e:
            return f"Git DevOps Error: {e}"

    def list_docker_containers(self):
        """Lists active docker containers"""
        try:
            client = docker.from_env()
            containers = client.containers.list()
            if not containers:
                return "DevOps: No active Docker containers running."
            names = [c.name for c in containers]
            return f"Active Containers: {', '.join(names)}"
        except Exception as e:
            return f"Docker Module Error: {e} (Is Docker Desktop running?)"


def devops_update(command):
    de = DevOpsEngine()
    if "commit" in command or "git" in command:
        return de.commit_and_push()
    if "docker" in command or "container" in command:
        return de.list_docker_containers()
    return "DevOps Engine online. Commands: commit, docker."
