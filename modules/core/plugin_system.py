import importlib.util
import os
import sys

PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "plugins")

_loaded_plugins = {}


def _ensure_plugins_dir():
    if not os.path.isdir(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR, exist_ok=True)
        with open(os.path.join(PLUGINS_DIR, "__init__.py"), "w") as f:
            f.write("")


def load_plugin(name: str) -> str:
    _ensure_plugins_dir()
    plugin_path = os.path.join(PLUGINS_DIR, f"{name}.py")
    if not os.path.isfile(plugin_path):
        available = list_plugins()
        return f"Plugin '{name}' not found. Available: {available}"
    try:
        spec = importlib.util.spec_from_file_location(name, plugin_path)
        if spec is None or spec.loader is None:
            return f"Failed to load plugin '{name}'."
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        funcs = []
        for attr_name in dir(module):
            if attr_name.startswith("friday_"):
                funcs.append(attr_name)
        _loaded_plugins[name] = {"module": module, "functions": funcs}
        return f"Plugin '{name}' loaded. Exports: {', '.join(funcs)}"
    except Exception as e:
        return f"Plugin load error: {e}"


def unload_plugin(name: str) -> str:
    if name in _loaded_plugins:
        del _loaded_plugins[name]
        if name in sys.modules:
            del sys.modules[name]
        return f"Plugin '{name}' unloaded."
    return f"Plugin '{name}' not loaded."


def list_plugins() -> str:
    _ensure_plugins_dir()
    files = [
        f[:-3]
        for f in os.listdir(PLUGINS_DIR)
        if f.endswith(".py") and f != "__init__.py"
    ]
    if not files:
        return "No plugins available. Create .py files in the plugins/ directory."
    return "Available plugins: " + ", ".join(files)


def run_plugin_function(plugin_name: str, func_name: str = "", *args) -> str:
    if plugin_name not in _loaded_plugins:
        result = load_plugin(plugin_name)
        if "Error" in result or "not found" in result:
            return result
    plugin = _loaded_plugins.get(plugin_name)
    if not plugin:
        return f"Plugin '{plugin_name}' not loaded."
    if not func_name:
        funcs = plugin["functions"]
        if funcs:
            func_name = funcs[0]
        else:
            return f"Plugin '{plugin_name}' has no friday_* functions."
    func = getattr(plugin["module"], func_name, None)
    if not func:
        return f"Function '{func_name}' not found in plugin '{plugin_name}'."
    try:
        result = func(*args)
        return str(result)
    except Exception as e:
        return f"Plugin function error: {e}"


def list_loaded_plugins() -> str:
    if not _loaded_plugins:
        return "No plugins loaded."
    return "Loaded plugins: " + ", ".join(
        f"{name} ({len(info['functions'])} functions)"
        for name, info in _loaded_plugins.items()
    )
