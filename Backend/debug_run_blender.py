"""
예제 스크립트로 블렌더 러너 테스트 
"""
from pathlib import Path
from blender_runner import run_blender_script

BASE = Path(__file__).resolve().parent.parent
script = BASE / "backend" / "sample_cube.py"
output = BASE / "generated_models" / "test_cube.glb"

output.parent.mkdir(exist_ok=True)

run_blender_script(str(script), str(output))
print("Output:", output)
