from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import time
from llm_ollama import generate_blender_script
from blender_exec import run_blender_script

app = Flask(__name__)

# 1. 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_SCRIPTS_DIR = os.path.join(BASE_DIR, 'outputs', 'scripts')
OUTPUT_IMAGES_DIR = os.path.join(BASE_DIR, 'outputs', 'images')

# 디렉토리 생성
os.makedirs(OUTPUT_SCRIPTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"success": False, "error": "No prompt provided"})

    print(f"Generating code for: {prompt}")
    script_code = generate_blender_script(prompt)
    
    if not script_code:
        return jsonify({"success": False, "error": "Failed to generate script"})

    # 2. 이미지 저장 경로 설정
    timestamp = int(time.time())
    image_filename = f"render_{timestamp}.png"
    abs_image_path = os.path.join(OUTPUT_IMAGES_DIR, image_filename).replace("\\", "/")

    # ========================================================
    # [확인하세요] 이 부분이 '뷰포트 정렬'이 아니라 '렌더링'이어야 합니다!
    # ========================================================
    render_code = f"""
import bpy
import os

# 1. 렌더링 엔진 설정 (Eevee)
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'

# 2. 기존 카메라/조명 삭제
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

for obj in bpy.data.objects:
    if obj.type in ['CAMERA', 'LIGHT']:
        bpy.data.objects.remove(obj, do_unlink=True)

# 3. 카메라 추가 (bpy.data 방식)
cam_data = bpy.data.cameras.new("RenderCam")
cam_obj = bpy.data.objects.new("RenderCam", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

cam_obj.location = (7, -7, 6)
cam_obj.rotation_euler = (0.9, 0, 0.785)

# 4. 조명 추가
light_data = bpy.data.lights.new("SunLight", type='SUN')
light_data.energy = 5
light_obj = bpy.data.objects.new("SunLight", light_data)
bpy.context.scene.collection.objects.link(light_obj)
light_obj.location = (5, 5, 10)

# 5. 파일 저장 설정
bpy.context.scene.render.filepath = r"{abs_image_path}"
bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 600
bpy.context.scene.render.image_settings.file_format = 'PNG'

# 6. 렌더링 실행 (사진 찍기)
print(">>> RENDER START")
try:
    bpy.ops.render.render(write_still=True)
    print(">>> RENDER SUCCESS")
except Exception as e:
    print(f">>> RENDER ERROR: {{e}}")
"""

    # [핵심] script_code 뒤에 render_code를 붙입니다.
    final_script = script_code + "\n" + render_code

    # 스크립트 저장
    script_filename = f"script_{timestamp}.py"
    script_path = os.path.join(OUTPUT_SCRIPTS_DIR, script_filename)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(final_script)

    # 블렌더 실행
    print("Launching Blender...")
    success, msg = run_blender_script(script_path, abs_image_path)
    
    if not success:
        return jsonify({"success": False, "error": msg})

    # 3. 이미지 대기 (Polling)
    print("Waiting for image...")
    for _ in range(30):
        if os.path.exists(abs_image_path):
            print("Image Created!")
            return jsonify({
                "success": True, 
                "image_url": f"/outputs/images/{image_filename}",
                "message": "Render Complete!"
            })
        time.sleep(1)

    return jsonify({"success": True, "image_url": "", "message": "Timeout: Image not created."})

@app.route('/outputs/images/<filename>')
def serve_image(filename):
    return send_from_directory(OUTPUT_IMAGES_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)