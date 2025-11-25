import bpy
import sys

def build_scene():
    # 초기화: 빈 씬으로 시작
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # === USER CODE START ===
    import bpy

    def build_scene():
    # Create a cube for the table top
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))

    # Create four leg cubes
    leg_size = 0.5
    leg_height = 2

    bpy.ops.mesh.primitive_cube_add(size=leg_size, location=(-1, -1, 0))
    bpy.ops.mesh.primitive_cube_add(size=leg_size, location=(1, -1, 0))
    bpy.ops.mesh.primitive_cube_add(size=leg_size, location=(-1, 1, 0))
    bpy.ops.mesh.primitive_cube_add(size=leg_size, location=(1, 1, 0))

    # Call the function to build the scene
    build_scene()
    # === USER CODE END ===

def main(output_path: str):
    build_scene()
    # glb로 익스포트 (Blender 5 기준)
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_cameras=False,
        export_lights=False,
    )

if __name__ == "__main__":
    argv = sys.argv
    out = argv[argv.index("--") + 1]
    main(out)
