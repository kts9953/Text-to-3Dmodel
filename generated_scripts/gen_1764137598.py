import bpy
import sys

def build_scene():
    # === USER CODE START ===
    # Seat
    bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, 0, 0.6))
    seat = bpy.context.active_object
    seat.scale[2] = 0.2
    seat.name = "Seat"

    # Backrest
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.5, 1.1))
    backrest = bpy.context.active_object
    backrest.scale[0] = 0.6
    backrest.scale[2] = 0.5
    backrest.name = "Backrest"

    # Left armrest
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.65, 0, 0.9))
    arm_L = bpy.context.active_object
    arm_L.scale[0] = 0.1
    arm_L.scale[1] = 0.5
    arm_L.scale[2] = 0.4
    arm_L.name = "Armrest_Left"

    # Right armrest
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.65, 0, 0.9))
    arm_R = bpy.context.active_object
    arm_R.scale[0] = 0.1
    arm_R.scale[1] = 0.5
    arm_R.scale[2] = 0.4
    arm_R.name = "Armrest_Right"

    # Legs
    leg_positions = [(0.45, 0.45, 0.3), (-0.45, 0.45, 0.3), (0.45, -0.45, 0.3), (-0.45, -0.45, 0.3)]
    for i, pos in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cube_add(size=0.3, location=pos)
        leg = bpy.context.active_object
        leg.scale[0] = 0.1
        leg.scale[1] = 0.1
        leg.scale[2] = 0.3
        leg.name = f"Leg_{i}"
    # === USER CODE END ===


def main(output_path: str):
    # 1) 씬 초기화 (딱 한 번)
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 2) glTF 익스포터 애드온 활성화
    try:
        bpy.ops.preferences.addon_enable(module="io_scene_gltf2")
    except Exception as e:
        print("[BlenderScript] Failed to enable glTF addon:", e)

    # 3) 유저가 정의한 씬 빌드
    build_scene()

    # 4) GLB로 익스포트
    
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_cameras=False,
        export_lights=False,
        use_selection=False,
    )


if __name__ == "__main__":
    argv = sys.argv

    # 안전하게 argv 파싱
    out = "output.glb"
    if "--" in argv:
        idx = argv.index("--") + 1
        if idx < len(argv):
            out = argv[idx]

    main(out)
