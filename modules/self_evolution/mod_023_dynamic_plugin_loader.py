import importlib.util
import os
import sys


def load_plugin(module_path: str):
    abs_path = os.path.abspath(module_path)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"Plugin not found: {abs_path}")

    module_name = os.path.splitext(os.path.basename(abs_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {abs_path}")

    module = importlib.util.module_from_spec(spec)
    existing = sys.modules.get(module_name)
    if existing:
        return existing

    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def reload_plugin(module):
    import importlib

    importlib.reload(module)
    return module
