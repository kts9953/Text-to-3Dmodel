import bpy
import sys

def build_scene():
    # 초기화: 빈 씬으로 시작
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # === USER CODE START ===
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1), radius=1)
        seat = bpy.context.object
        seat.name = 'Seat'
        seat.dimensions = (2, 2, 0.5)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, location=(0, -1, 1))
        backrest = bpy.context.object
        backrest.name = 'Backrest'
        backrest.dimensions = (2, 4, 2)
        backrest.rotation_euler = (0, math.pi/2, 0)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, location=(0, -1.5, 1))
        legs = bpy.context.object
        legs.name = 'Legs'
        legs.dimensions = (2, 4, 1)
        legs.rotation_euler = (0, math.pi/2, 0)

        bpy.ops.mesh.primitive_sphere_add(location=(0, -0.5, 1), radius=0.25)
        armrest_l = bpy.context.object
        armrest_l.name = 'Armrest Left'
        armrest_l.dimensions = (0.5, 0.5, 2)

        bpy.ops.mesh.primitive_sphere_add(location=(0, -1.75, 1), radius=0.25)
        armrest_r = bpy.context.object
        armrest_r.name = 'Armrest Right'
        armrest_r.dimensions = (0.5, 0.5, 2)
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
