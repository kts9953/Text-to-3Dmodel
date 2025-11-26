# Backend/codegen.py
from pathlib import Path
import re
from code_template import BASE_TEMPLATE
import textwrap

def normalize_indentation(user_code: str) -> str:
    """
    LLM이 생성한 코드의 들여쓰기를 정규화해서
    모든 줄의 공통 최소 들여쓰기를 제거함.
    """
    code = textwrap.dedent(user_code)

    # 2. 모든 줄 왼쪽 공백 제거(완전 평탄화)
    # lines = []
    #for line in code.splitlines():
    #    if line.strip() == "":
    #        lines.append("")  # 빈 줄은 유지
    #    else:
    #        lines.append(line.lstrip())

    return code.strip("\n")

def indent_user_code(user_code: str) -> str:
    """user_code를 build_scene() 안쪽에 맞게 들여쓰기."""
    lines = user_code.splitlines()
    indented_lines = []
    for line in lines:
        if line.strip():
            indented_lines.append("    " + line)  # 4스페이스
        else:
            indented_lines.append("")  # 빈 줄 유지
    return "\n".join(indented_lines)


def build_full_script_from_user_code(user_code: str) -> str:
    """템플릿에 user_code를 끼워 넣어서 전체 Blender 스크립트 생성."""
    extracted = extract_code_from_llm_output(user_code)
    norm_indent = normalize_indentation(extracted)
    print(norm_indent)
    indented = indent_user_code(norm_indent)
    return BASE_TEMPLATE.format(user_code=indented)


def save_script(full_script: str, scripts_dir: str | Path, basename: str) -> Path:
    """generated_scripts 안에 basename.py로 저장하고 경로 리턴."""
    scripts_dir = Path(scripts_dir)
    scripts_dir.mkdir(parents=True, exist_ok=True)
    file_path = scripts_dir / f"{basename}.py"
    file_path.write_text(full_script, encoding="utf-8")
    return file_path


def extract_code_from_llm_output(text: str) -> str:
    """
    LLM 응답에서 ```python ... ``` 블록 안 코드만 뽑아냄.
    프롬프트에서 '반드시 하나의 python 코드블럭만 사용'한다고 가정.
    """
    fence_pattern = r"```(?:python)?\s*(.*?)```"
    matches = re.findall(fence_pattern, text, re.DOTALL | re.IGNORECASE)

    if not matches:
        # 프롬프트 계약이 깨진 경우 -> 여기서 바로 에러 내고 상위에서 처리
        raise ValueError("LLM output does not contain a ```python ... ``` code block.")

    # 혹시 공백 블럭이 섞여 있어도, 첫 번째 non-empty 블럭을 쓰도록 방어
    for code in matches:
        stripped = code.strip()
        if stripped:
            return stripped

    # 전부 공백이면 그냥 첫 번째라도 반환
    return matches[0].strip()