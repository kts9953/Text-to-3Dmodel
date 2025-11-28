"""
debug_run_blender.py에서 사용하는 예제 스크립트
"""
import bpy
import sys

def main(output_path: str):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_cube_add(size=1)
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_cameras=False,
        export_lights=False,
    )

if __name__ == "__main__":
    argv = sys.argv
    out = argv[argv.index("--") + 1]
    main(out)
