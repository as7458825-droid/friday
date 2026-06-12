from dotenv import load_dotenv
load_dotenv()

from modules.integrations.blender_controller import run_blender_script

script = '''
import bpy
bpy.ops.mesh.primitive_cube_add(size=2)
print("Cube created")
'''

result = run_blender_script(script, background=True)
print(result)