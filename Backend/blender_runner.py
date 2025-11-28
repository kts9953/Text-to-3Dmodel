import subprocess
import os
import platform
from pathlib import Path

def get_blender_path() -> str:
    """
    Blender 실행 파일 경로를 반환하는 헬퍼 함수.

    우선순위:
    1. 환경변수 BLENDER_PATH 가 설정되어 있으면 그 경로 사용
    2. OS(platform.system())에 따라 기본 설치 경로 사용
    3. 둘 다 안 맞으면 RuntimeError 발생
    """

    env_path = os.getenv("BLENDER_PATH")
    if env_path:
        return env_path
    
    
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
    """
    주어진 Blender 파이썬 스크립트를 백그라운드 모드로 실행해서
    지정된 output_path 에 결과 파일(GLB/PNG 등)을 생성하는 함수.

    Parameters
    ----------
    script_path : str
        Blender 안에서 실행할 파이썬 스크립트(.py) 경로.
        스크립트 내부에서는 sys.argv 를 통해 output_path 를 파라미터로 받을 수 있음.
    output_path : str
        Blender 가 결과를 저장할 파일 경로.
        (예: GLB, PNG 등. 실제 포맷은 스크립트 내용에 따라 달라짐)

    Raises
    ------
    RuntimeError
        Blender 프로세스가 비정상 종료(returncode != 0) 했을 때 발생.
    """
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
