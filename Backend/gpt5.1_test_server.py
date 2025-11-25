
from pathlib import Path
from llm_ollama import generate_user_code
from codegen import build_full_script_from_user_code, save_script
from blender_runner import run_blender_script
import time

BASE = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE / "generated_scripts"
MODELS_DIR = BASE / "generated_models"
GPT5_SCRIPT_PATH = BASE / "GPT5_scripts" / "user_code.py"

def main():
    print("=== Mini Server (LLM → Blender) ===")

    user_code = GPT5_SCRIPT_PATH.read_text(encoding="utf-8")
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
