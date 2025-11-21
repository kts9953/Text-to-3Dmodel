# Backend/debug_gen_with_template.py
from pathlib import Path
from llm_ollama import generate_user_code
from blender_runner import run_blender_script
from codegen import build_full_script_from_user_code, save_script

# 프로젝트 루트 (D:\Text to 3D\ 가 되도록 조정)
BASE = Path(__file__).resolve().parent.parent

SCRIPTS_DIR = BASE / "generated_scripts"
MODELS_DIR = BASE / "generated_models"


def main():
    # 여기 user_code가 나중에 LLM이 만들어줄 부분이라고 생각하면 됨
    prompt = "a table with four legs"
    user_code = generate_user_code(prompt)

    # 1) 전체 Blender 스크립트 문자열 생성
    full_script = build_full_script_from_user_code(user_code)
    script_path = save_script(full_script, SCRIPTS_DIR, "gen_from_llm")
    
    # 2) generated_scripts 안에 저장
    script_path = save_script(full_script, SCRIPTS_DIR, basename="test_from_template")
    print("[debug] script_path:", script_path)

    # 3) Blender 실행해서 glb 생성
    output_path = MODELS_DIR / "test_from_template.glb"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    run_blender_script(str(script_path), str(output_path))

    print("[debug] Output glb:", output_path)


if __name__ == "__main__":
    main()
