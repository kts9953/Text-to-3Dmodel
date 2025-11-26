import bpy
import sys

def build_scene():
    # === USER CODE START ===
    # Seat
    bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0.0, 0.0, 0.5))
    seat = bpy.context.active_object
    seat.scale[2] = 0.2
    seat.name = "Seat"

    # Backrest
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.45, 1.0))
    backrest = bpy.context.active_object
    backrest.scale[0] = 0.6
    backrest.scale[2] = 0.5
    backrest.name = "Backrest"

    # Left leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(0.45, 0.35, 0.3))
    leg_LF = bpy.context.active_object
    leg_LF.name = "Leg_LeftFront"

    # Right leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(-0.45, 0.35, 0.3))
    leg_RF = bpy.context.active_object
    leg_RF.name = "Leg_RightFront"

    # Left back leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(0.45, -0.35, 0.3))
    leg_LB = bpy.context.active_object
    leg_LB.name = "Leg_LeftBack"

    # Right back leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.6, location=(-0.45, -0.35, 0.3))
    leg_RB = bpy.context.active_object
    leg_RB.name = "Leg_RightBack"
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
