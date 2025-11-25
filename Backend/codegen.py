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
    나중에 LLM 붙일 때 사용.
    ```python ... ``` 블록 안 코드만 뽑아냄.
    """
    fence_pattern = r"```(?:python)?\s*(.*?)```"
    m = re.search(fence_pattern, text, re.DOTALL | re.IGNORECASE)
    if m:
        code = m.group(1)
    else:
        code = text
    return code.strip()
