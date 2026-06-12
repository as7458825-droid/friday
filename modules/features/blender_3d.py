import os
import subprocess
import tempfile

BLENDER_PATH = os.getenv("BLENDER_PATH", "blender")


def _run_blender_script(script: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(script)
            f.flush()
            result = subprocess.run(
                [BLENDER_PATH, "--background", "--python", f.name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            os.unlink(f.name)
            if result.returncode == 0:
                return result.stdout.strip() or "Blender command executed."
            return f"Blender error: {result.stderr[:200]}"
    except FileNotFoundError:
        return "Blender not found. Set BLENDER_PATH in .env or install Blender."
    except subprocess.TimeoutExpired:
        return "Blender execution timed out."
    except Exception as e:
        return f"Blender error: {e}"


def create_cube(size: float = 2.0) -> str:
    script = """
import bpy
bpy.ops.mesh.primitive_cube_add(size={size})
print("Cube created.")
"""
    return _run_blender_script(script)


def create_sphere(radius: float = 1.0) -> str:
    script = """
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(radius={radius})
print("Sphere created.")
"""
    return _run_blender_script(script)


def create_cylinder(radius: float = 1.0, depth: float = 2.0) -> str:
    script = """
import bpy
bpy.ops.mesh.primitive_cylinder_add(radius={radius}, depth={depth})
print("Cylinder created.")
"""
    return _run_blender_script(script)


def delete_all() -> str:
    script = """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
print("All objects deleted.")
"""
    return _run_blender_script(script)


def export_stl(output_path: str = "") -> str:
    if not output_path:
        output_path = os.path.join(os.path.dirname(__file__), "..", "..", "output.stl")
    script = """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_mesh.stl(filepath='{output_path}')
print("Exported to {output_path}")
"""
    return _run_blender_script(script)


def render(output_path: str = "") -> str:
    if not output_path:
        output_path = os.path.join(os.path.dirname(__file__), "..", "..", "render.png")
    script = """
import bpy
bpy.context.scene.render.filepath = '{output_path}'
bpy.ops.render.render(write_still=True)
print("Rendered to {output_path}")
"""
    return _run_blender_script(script)


def run_custom(blender_code: str) -> str:
    return _run_blender_script(blender_code)


def status() -> str:
    try:
        result = subprocess.run(
            [BLENDER_PATH, "--version"], capture_output=True, text=True, timeout=5
        )
        version = result.stdout.split("\n")[0] if result.stdout else "Unknown"
        return f"Blender found: {version}"
    except Exception:
        return (
            "Blender not found. Install from blender.org and set BLENDER_PATH in .env"
        )
