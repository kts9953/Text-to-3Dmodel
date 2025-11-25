# backend/llm_ollama.py
import requests
from codegen import extract_code_from_llm_output  # 이미 너 구조에 있음

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"

SYSTEM_PROMPT = """
You are an expert in Blender bpy scripting.

Your task: 
Generate ONLY the Python code that will go inside a function called build_scene().
DO NOT include:
- import statements
- full script
- main function
- rendering
- exporting
- scene reset

Assume:
- bpy is already imported
- the scene is already reset with: bpy.ops.wm.read_factory_settings(use_empty=True)
- You are inside:

    def build_scene():
        # === USER CODE START ===
        (your code here)
        # === USER CODE END ===

Rules:
1. Create solid geometry only (cubes, spheres, cylinders, cones, etc.)
2. Avoid wireframes.
3. Position objects as needed.
4. Keep the code short, readable, and valid Python.
"""

def generate_user_code(prompt: str) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Request:\n{prompt}\n\n# Python code only:"

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        print("[LLM] Requesting Blender code...")
        r = requests.post(OLLAMA_URL, json=payload)
        r.raise_for_status()

        raw = r.json().get("response", "")
        code = extract_code_from_llm_output(raw)
        print("[LLM] Code generated length:", len(code))
        return code

    except Exception as e:
        print("[LLM ERROR]", e)
        return ""
