import os

from git import Repo, InvalidGitRepositoryError


def _get_repo(path: str = ".") -> Repo:
    abs_path = os.path.abspath(path)
    return Repo(abs_path)


def git_init(path: str = ".") -> str:
    abs_path = os.path.abspath(path)
    if os.path.isdir(os.path.join(abs_path, ".git")):
        return f"Git repo already exists at {abs_path}"
    Repo.init(abs_path)
    return f"Initialized empty Git repo at {abs_path}"


def git_commit(message: str) -> str:
    try:
        repo = _get_repo()
        repo.git.add(A=True)
        repo.index.commit(message)
        return f"Committed: {message}"
    except InvalidGitRepositoryError:
        return "Not a git repository"
    except Exception as e:
        return f"Commit failed: {e}"


def git_push(remote: str = "origin", branch: str = None) -> str:
    try:
        repo = _get_repo()
        if branch is None:
            branch = repo.active_branch.name
        origin = repo.remotes[remote]
        origin.push(branch)
        return f"Pushed to {remote}/{branch}"
    except InvalidGitRepositoryError:
        return "Not a git repository"
    except Exception as e:
        return f"Push failed: {e}"


def git_pull(remote: str = "origin", branch: str = None) -> str:
    try:
        repo = _get_repo()
        if branch is None:
            branch = repo.active_branch.name
        origin = repo.remotes[remote]
        origin.pull(branch)
        return f"Pulled from {remote}/{branch}"
    except InvalidGitRepositoryError:
        return "Not a git repository"
    except Exception as e:
        return f"Pull failed: {e}"


def git_status() -> list[str]:
    try:
        repo = _get_repo()
        if repo.is_dirty():
            lines = ["Unstaged changes:"]
            for item in repo.index.diff(None):
                lines.append(f"  modified: {item.a_path}")
            for item in repo.untracked_files:
                lines.append(f"  untracked: {item}")
            return lines
        return ["Working tree clean"]
    except InvalidGitRepositoryError:
        return ["Not a git repository"]
    except Exception as e:
        return [f"Status error: {e}"]
