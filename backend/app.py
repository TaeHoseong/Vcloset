from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from nanobanana import run_virtual_tryon

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)
app = Flask(__name__)

ALLOWED_ORIGINS = ["http://127.0.0.1:5500", "https://vcloset.netlify.app"]

CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response
  
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)