"""
OPENAPI로 전체 파이프라인 테스트
"""
from pathlib import Path
from llm_gpt import generate_user_code
from codegen import build_full_script_from_user_code, save_script
from blender_runner import run_blender_script
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE / "generated_scripts"
MODELS_DIR = BASE / "generated_models"

def main():
    print("=== Mini Server (LLM → Blender) ===")

    # 🔸 사용자 프롬프트 입력 받기
    user_prompt = input("Describe your scene (e.g. 'make me a chair'): ").strip()

    # 1) LLM 호출 → build_scene() 내부 코드 받아오기
    user_code = generate_user_code(user_prompt)
    print("\n=== [LLM OUTPUT user_code] ===")
    print(user_code)
    print("==============================\n")

    # 2) 전체 파이썬 스크립트 생성 (템플릿에 끼워넣기)
    full_script = build_full_script_from_user_code(user_code)

    # 3) .py 파일로 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    script_path = save_script(full_script, SCRIPTS_DIR, f"gen_{timestamp}")
    print("[MiniServer] Script saved:", script_path)

    # 4) Blender 실행 → GLB 저장
    output_path = MODELS_DIR / f"model_{timestamp}.glb"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("[MiniServer] Running Blender...")
    run_blender_script(str(script_path), str(output_path))

    print("[MiniServer] ✅ GLB saved at:", output_path)


if __name__ == "__main__":
    main()
