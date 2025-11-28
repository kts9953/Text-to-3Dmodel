"""
llm출력을 끼워넣을 베이스 템플릿
"""
BASE_TEMPLATE = """\
import bpy
import sys

def build_scene():
    # === USER CODE START ===
{user_code}
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
"""
