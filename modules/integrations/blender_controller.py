import subprocess
import os
import logging

log = logging.getLogger("FRIDAY.Blender")

# Aapka provide kiya gaya path
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"

def run_blender_script(python_script_content: str, background: bool = True) -> str:
    """
    Blender ke andar Python script run karta hai.
    """
    if not os.path.exists(BLENDER_PATH):
        return f"Error: Blender executable nahi mila is path par: {BLENDER_PATH}"

    # Temporary script file banana
    temp_script = os.path.join(os.getcwd(), "temp_blender_script.py")
    with open(temp_script, "w") as f:
        f.write(python_script_content)

    try:
        cmd = [BLENDER_PATH]
        if background:
            cmd.append("--background")
        cmd.extend(["--python", temp_script])

        log.info(f"Running Blender task...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            return "Blender task successfully completed!"
        else:
            return f"Blender Error: {result.stderr}"
    except Exception as e:
        return f"Failed to connect to Blender: {e}"
    finally:
        if os.path.exists(temp_script):
            os.remove(temp_script)

def create_simple_cube():
    """Example: Blender mein ek cube banane ki script."""
    script = """
import bpy
# Purane objects delete karein
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
# Naya cube banayein
bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
# Save karein (optional)
# bpy.ops.wm.save_as_mainfile(filepath="friday_3d_output.blend")
"""
    return run_blender_script(script, background=False) # background=False taaki aapko Blender khulta hua dikhe
