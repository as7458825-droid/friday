from __future__ import annotations
from typing import Callable, Optional

_registry: dict[str, Callable] = {}


def register_tool(name: str, func: Callable) -> None:
    _registry[name] = func


def get_tool(name: str) -> Optional[Callable]:
    return _registry.get(name)


def get_all_tools() -> dict[str, Callable]:
    return dict(_registry)


def list_tools() -> list[str]:
    return sorted(_registry.keys())
