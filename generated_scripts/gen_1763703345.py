import bpy
import sys

def build_scene():
    # 초기화: 빈 씬으로 시작
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # === USER CODE START ===
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), radius=1)
    bpy.context.object.name = "Apple"

    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.translate(value=(-0.5, 0, -0.5))

    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0), radius=0.2, depth=1)
    bpy.context.object.name = "Core"

    bpy.ops.transform.move(x=-0.5, y=0, z=-0.3)

    bpy.ops.mesh.primitive_sphere_add(location=(0, 0, 0), radius=0.05)
    bpy.context.object.name = "Stem"
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
