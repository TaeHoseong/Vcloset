from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv
import sys
from supabase import create_client, Client
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from nanobanana import run_virtual_tryon

app = Flask(__name__)

load_dotenv()

# Nanobanana
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# Supabase
SUPABASE_URL = "https://ebwzvgtkgpaoqizcltfu.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ALLOWED_ORIGINS = ["http://127.0.0.1:5500", "https://vcloset.netlify.app"]

CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

@app.route("/", methods=["GET"])
def home():
    return "OK", 200
  
@app.route("/tryon", methods=["POST", "OPTIONS"])
def tryon():
    if request.method == "OPTIONS":
        origin = request.headers.get("Origin")
        res = jsonify({"message": "preflight ok"})
        if origin in ALLOWED_ORIGINS:
            res.headers["Access-Control-Allow-Origin"] = origin
        res.headers["Access-Control-Allow-Headers"] = "*"
        res.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return res, 200
      
    try:
        if "person" not in request.files or "garment" not in request.files:
            return jsonify({"error": "person and garment files are required"}), 400

        person_file = request.files["person"]
        garment_file = request.files["garment"]

        person_img = Image.open(person_file.stream).convert("RGB")
        garment_img = Image.open(garment_file.stream).convert("RGB")

        result_img = run_virtual_tryon(person_img, garment_img)
        
        buffer = io.BytesIO()
        result_img.save(buffer, format="PNG")
        buffer.seek(0)
        img_b64 = base64.b64encode(buffer.read()).decode("utf-8")

        return jsonify({"image_base64": img_b64})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    
@app.post("/api/upload_body_image")
def upload_body_image():
    email = request.form.get("email")
    file = request.files.get("file")
    uid = request.form.get("user_id")
    if not email or not file:
        return jsonify({"error": "missing data"}), 400

    # 파일명 & 저장 경로(스토리지 내부 경로)
    filename = secure_filename(file.filename)
    storage_path = f"body_images/{uid}/{filename}"   # bucket 안의 경로

    # 1) FileStorage → bytes 로 읽기
    file_bytes = file.read()

    try:
        
        # 2) Supabase Storage 업로드
        res = supabase.storage.from_("vcloset").upload(
            path=storage_path,
            file=file_bytes,
            file_options={
                "content-type": file.mimetype,
                "upsert": "true",
            },
        )
    except Exception as e:
        return jsonify({"error": "파일 업로드 실패", "detail": str(e)}), 500

    # 3) public URL 생성
    public_url = supabase.storage.from_("vcloset").get_public_url(storage_path)

    # 4) user_metadata에 body_image_url 저장 (service_role 키 필요)
    try:
        supabase.auth.admin.update_user_by_id(
            uid,
            {
                "user_metadata": {
                    "body_image_url": public_url,
                }
            },
        )
    except Exception as e:
        return jsonify({"error": "유저 메타데이터 업데이트 실패", "detail": str(e)}), 500

    return jsonify({
        "message": "업로드 완료!",
        "body_image_url": public_url,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)