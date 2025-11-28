"""
ollama 사용하는 전체 파이프라인 테스트
"""
from pathlib import Path
from llm_ollama import generate_user_code
from codegen import build_full_script_from_user_code, save_script
from blender_runner import run_blender_script
import time

BASE = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE / "generated_scripts"
MODELS_DIR = BASE / "generated_models"


def main():
    print("=== Mini Server (LLM → Blender) ===")
    prompt = input("프롬프트 입력: ")

    if not prompt.strip():
        print("[ERROR] 프롬프트가 비어있음")
        return
    
    # 1) LLM에서 user_code 생성
    user_code = generate_user_code(prompt)
    if not user_code:
        print("[ERROR] LLM 코드 생성 실패")
        return

    print("\n=== [LLM OUTPUT user_code] ===")
    print(user_code)
    print("==============================\n")

    # 2) 템플릿 합성
    full_script = build_full_script_from_user_code(user_code)

    # 3) python 스크립트 저장
    timestamp = int(time.time())
    script_path = save_script(full_script, SCRIPTS_DIR, f"gen_{timestamp}")
    print("[MiniServer] Script saved:", script_path)

    # 4) Blender 실행 → GLB 출력
    output_path = MODELS_DIR / f"model_{timestamp}.glb"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("[MiniServer] Running Blender...")
    run_blender_script(str(script_path), str(output_path))

    print("[MiniServer] GLB saved at:", output_path)


if __name__ == "__main__":
    main()
