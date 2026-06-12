_registry: dict[str, callable] = {}


def register_tool(name: str, func: callable) -> None:
    _registry[name] = func


def get_tool(name: str) -> callable | None:
    return _registry.get(name)


def get_all_tools() -> dict[str, callable]:
    return dict(_registry)


def list_tools() -> list[str]:
    return sorted(_registry.keys())
