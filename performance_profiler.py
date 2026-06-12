"""
FRIDAY — Performance Profiler
Identifies bottlenecks using cProfile and memory_profiler.
Logs results to logs/performance/ and suggests optimizations.

Usage:
    python performance_profiler.py              # run all profiles
    python performance_profiler.py --quick      # skip heavy modules
"""

import cProfile
import importlib
import io
import os
import pstats
import sys
import time
import tracemalloc
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

LOG_DIR = os.path.join(PROJECT_ROOT, "logs", "performance")
os.makedirs(LOG_DIR, exist_ok=True)


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")
    with open(os.path.join(LOG_DIR, "profile.log"), "a") as f:
        f.write(f"[{ts}] {msg}\n")


def profile_import(module_name: str) -> float:
    """Time how long a module takes to import."""
    start = time.perf_counter()
    try:
        importlib.import_module(module_name)
    except Exception as e:
        log(f"  WARN {module_name} import failed: {e}")
        return -1
    elapsed = time.perf_counter() - start
    return elapsed


def profile_function(func, *args, name: str = None, iterations: int = 100):
    """Profile a function call with cProfile."""
    fname = name or getattr(func, "__name__", "unknown")
    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(iterations):
        try:
            func(*args)
        except Exception:
            pass
    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumtime")
    ps.print_stats(10)

    log(f"  {fname} ({iterations} calls):")
    for line in s.getvalue().strip().split("\n")[-10:]:
        log(f"    {line.strip()}")

    return s.getvalue()


def profile_memory(label: str):
    """Snapshot memory usage before/after a block."""
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()

    def _finish():
        snapshot2 = tracemalloc.take_snapshot()
        stats = snapshot2.compare_to(snapshot1, "lineno")
        total = sum(s.size_diff for s in stats)
        log(f"  {label}: {total / 1024:.1f} KB delta")
        top = stats[:5]
        for s in top:
            log(f"    {s.size_diff / 1024:.1f} KB  {s.traceback}")
        tracemalloc.stop()

    return _finish


def suggest_optimizations(profile_data: dict):
    """Analyze profile data and suggest improvements."""
    suggestions = []
    heavy_modules = {
        k: v for k, v in profile_data.get("imports", {}).items() if v > 0.3
    }
    if heavy_modules:
        names = ", ".join(heavy_modules.keys())
        suggestions.append(
            f"Lazy load heavy modules: {names} "
            f"(each >300ms import time). "
            f"Move import inside command handlers."
        )

    if profile_data.get("chroma_startup", 0) > 0.5:
        suggestions.append(
            "ChromaDB startup is slow (>500ms). "
            "Pre-warm in background thread on startup."
        )

    if profile_data.get("tts_first_speak", 0) > 0.5:
        suggestions.append(
            "First TTS call is slow (>500ms). "
            "Pre-initialize pyttsx3 engine in background."
        )

    if suggestions:
        log("\nOPTIMIZATION SUGGESTIONS:")
        for s in suggestions:
            log(f"  * {s}")
    else:
        log("\nNo major bottlenecks detected.")


def run_all():
    log("=" * 55)
    log("FRIDAY Performance Profiler")
    log("=" * 55)

    profile_data = {"imports": {}}

    # -- module import times --
    log("\n[1/5] Measuring module import times...")
    heavy_candidates = [
        "core.voice",
        "modules.llm.openrouter_client",
        "modules.memory.vector_store",
        "modules.memory.user_memory",
        "modules.multi_agent.coordinator",
        "modules.browser_engine.mod_041_playwright_instance_core",
        "modules.vision.m451",
        "modules.media_studio.mod_031_silence_gap_trimmer",
        "modules.hud.mod_001_neon_window",
        "modules.self_evolution.mod_029_system_health_heartbeat",
        "modules.security_vault.mod_091_env_key_variable_encryptor",
        "modules.devops_compiler.mod_071_full_stack_code_generator",
        "modules.data_analytics.mod_081_pandas_csv_data_dataframe",
    ]
    for mod in heavy_candidates:
        try:
            t = profile_import(mod)
            if t >= 0:
                profile_data["imports"][mod] = t
                log(f"  {mod}: {t:.3f}s")
        except Exception as e:
            log(f"  WARN {mod} import failed: {e}")

    # -- ChromaDB startup --
    log("\n[2/5] ChromaDB startup...")
    start = time.perf_counter()
    try:
        import chromadb
        from chromadb.config import Settings

        chromadb.EphemeralClient(settings=Settings(anonymized_telemetry=False))
        profile_data["chroma_startup"] = time.perf_counter() - start
        log(f"  Ephemeral client: {profile_data['chroma_startup']:.3f}s")
    except Exception as e:
        log(f"  SKIP: {e}")

    # -- TTS engine init --
    log("\n[3/5] TTS engine init...")
    start = time.perf_counter()
    try:
        import pyttsx3

        engine = pyttsx3.init()
        profile_data["tts_init"] = time.perf_counter() - start
        log(f"  pyttsx3.init(): {profile_data['tts_init']:.3f}s")

        start = time.perf_counter()
        engine.say("test")
        engine.runAndWait()
        profile_data["tts_first_speak"] = time.perf_counter() - start
        log(f"  First say(): {profile_data['tts_first_speak']:.3f}s")
    except Exception as e:
        log(f"  SKIP: {e}")

    # -- LLM request timing --
    log("\n[4/5] LLM request (openrouter_client)...")
    try:
        from modules.llm.openrouter_client import ask_llm

        start = time.perf_counter()
        reply = ask_llm("Say OK in one word.")
        t = time.perf_counter() - start
        profile_data["llm_request"] = t
        log(f"  ask_llm: {t:.3f}s | reply: {reply[:60] if reply else 'None'}")
    except Exception as e:
        log(f"  SKIP: {e}")

    # -- suggestions --
    log("\n[5/5] Analysis...")
    suggest_optimizations(profile_data)

    log("\nProfile log written to: " + os.path.join(LOG_DIR, "profile.log"))
    return profile_data


if __name__ == "__main__":
    run_all()
