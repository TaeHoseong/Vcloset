from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from supabase import create_client, Client
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

app = Flask(__name__)

# CORS 설정
ALLOWED_ORIGINS = ["http://127.0.0.1:5500", "https://vcloset.netlify.app", "https://vcloset.netlify.app/#"]
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

load_dotenv()

# Supabase 설정 (환경변수로 관리 추천)
SUPABASE_URL = "https://ebwzvgtkgpaoqizcltfu.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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