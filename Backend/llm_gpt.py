"""
사용자 입력 받고 OpenAI api로 출력 반환
"""
from openai import OpenAI
from system_prompt_comp import SYSTEM_PROMPT
import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    # [EXE 모드] 실행 파일(.exe)이 있는 폴더를 기준점으로 잡음
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # [개발 모드] 이 파이썬 파일(llm_gpt.py)이 있는 폴더를 기준점으로 잡음
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# .env 파일의 절대 경로 생성
env_path = os.path.join(BASE_DIR, '.env')

# 해당 경로의 .env 파일을 강제로 읽어오기
load_dotenv(dotenv_path=env_path)

# API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_user_code(prompt :str) -> str:

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3)
    
    full_text = response.choices[0].message.content
    
    return full_text

