from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv
from nanobanana import run_virtual_tryon

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)
app = Flask(__name__)
CORS(app)

@app.route("/tryon", methods=["POST"])
def tryon():
  try:
    if "person" not in request.files or "garment" not in request.files:
      return jsonify({"error": "person and garment files are required"}), 400

    person_file = request.files["person"]
    garment_file = request.files["garment"]

    person_img = Image.open(person_file.stream).convert("RGB")
    garment_img = Image.open(garment_file.stream).convert("RGB")

    result_img = run_virtual_tryon(person_img, garment_img)
    
    # 이미지 → base64 문자열로 변환
    buffer = io.BytesIO()
    result_img.save(buffer, format="PNG")
    buffer.seek(0)
    img_bytes = buffer.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    return jsonify({"image_base64": img_b64})
  except Exception as e:
    print("Error:", e)
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=True)