"""
실제 서버
"""
import sys
import os
from flask import Flask, render_template, send_from_directory, request
from datetime import datetime
# 기존 모듈 import
from blender_runner import run_blender_script
from llm_gpt import generate_user_code
from codegen import build_full_script_from_user_code, save_script

# ---------------------------------------------------------------------------
# 1. 경로 설정 (최종 통합본)
# ---------------------------------------------------------------------------

#getattr(object, name, default=None) : 객체에서 속성을 확인 후 가져오는 함수

#sys에 'frozen' 속성이 있는지 확인.
#exe로 패키징 되었을 때는 sys.frozen이 True가 됨.

if getattr(sys, 'frozen', False):
    # [A. 납품용 EXE 모드]
    print(" [Mode] EXE 실행")
    
    #sys.executable : 현재 실행 중인 EXE 파일의 경로.
    #ex) C:\path\to\your_app.exe

    #os.path.dirname() : 경로에서 디렉토리 부분만 추출.
    BASE_DIR = os.path.dirname(sys.executable)
    
    #sys._MEIPASS : PyInstaller가 압축 푼 임시 폴더 경로.
    #exe 안의 templates 폴더에 접근하기 위함.
    INTERNAL_DIR = sys._MEIPASS

    #os.path.join(a,b) : 경로 조합 함수.
    #INTERNAL_DIR/templates 으로 만들어 줌.
    template_dir = os.path.join(INTERNAL_DIR, 'templates')
    
    #플라스크 앱 객체 생성.
    #기본은 ./templates인데, 여기서는 PyInstaller 임시 폴더의 templates를 사용.
    app = Flask(__name__, template_folder=template_dir)

else:
    # [B. 개발용 VS Code 모드]
    print(" [Mode] 개발용 Python 실행")
    
    # __file__ : 현재 server.py의 경로.(backend/server.py)
    #os.path .abspath(__file__) : 절대 경로로 변환.
    #os.path.dirname() : 그 경로에서 상위 디렉터리만 가져옴.
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # BASE_DIR : 프로젝트 전체 루트 (backend의 상위)
    BASE_DIR = os.path.dirname(CURRENT_DIR)
    
    app = Flask(__name__)

# ---------------------------------------------------------------------------
# 2. 파일 저장소 설정 (BASE_DIR 하나만 사용)
# ---------------------------------------------------------------------------

# model_file 폴더 경로 구하기 (BASE_DIR 기준으로만 사용)
MODEL_FILE_DIR = os.path.join(BASE_DIR, "generated_models")

# 파이썬(.py) 스크립트 저장소.
SCRIPTS_DIR = os.path.join(BASE_DIR, "generated_scripts")

# MODEL_FILE_DIR, SCRIPTS_DIR 폴더가 없으면 만듦.
os.makedirs(MODEL_FILE_DIR, exist_ok=True)
os.makedirs(SCRIPTS_DIR, exist_ok=True) 

print(f"실행 기준 경로: {BASE_DIR}")

# ---------------------------------------------------------------------------
# 3. 라우팅 및 기능 (기존 코드와 동일)
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/make_cube", methods=["POST"])
def make_cube():
    user_prompt = request.form.get("prompt")
    print(f"유저 입력: {user_prompt}")
    
    generated_code = generate_user_code(user_prompt)
    
    if not generated_code:
        return "AI가 코드를 생성하지 못했습니다."
    
    full_script = build_full_script_from_user_code(generated_code)
    
    script_path = save_script(full_script, SCRIPTS_DIR, "generated.py")
    output_path = os.path.join(MODEL_FILE_DIR, "generated_model.glb")

    if os.path.exists(output_path):
        try: os.remove(output_path)
        except: pass
        
    run_blender_script(script_path, output_path)

    return f"3D 모델이 생성되었습니다! <a href='/model_file/generated_model.glb' download>여기</a>를 클릭하여 다운로드하세요."

@app.route("/model_file/<path:filename>")
def server_model(filename):
    return send_from_directory(MODEL_FILE_DIR, filename)


if __name__ == "__main__":
    # EXE로 만들 때는 debug=False가 필수입니다.
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)