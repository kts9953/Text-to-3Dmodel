# backend/blender_runner.py
import subprocess
import os
import platform
from pathlib import Path

def get_blender_path() -> str:
    system = platform.system()
    if system == "Darwin":  # Mac
        return "/Applications/Blender.app/Contents/MacOS/Blender"
    elif system == "Linux":
        return "/usr/bin/blender"
    elif system == "Windows":
        return r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
    else:
        raise RuntimeError("Unsupported OS")

def run_blender_script(script_path: str, output_path: str) -> None:
    blender = get_blender_path()

    script_path = str(Path(script_path).resolve())
    output_path = str(Path(output_path).resolve())

    cmd = [
        blender,
        "-b",
        "-P", script_path,
        "--",
        output_path,    
    ]

    print("▶ Running Blender:")
    print("  ", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Blender Error:", result.stderr)
        raise RuntimeError("Blender script failed")

    print("Blender OK")
    print(result.stdout)
