from google import genai
from PIL import Image
import io
import os
import argparse
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# -------------------------------
# ❗ Virtual Try-On Function
# -------------------------------
def run_virtual_tryon(person_img: Image.Image, garment_img: Image.Image):
  client = genai.Client(api_key=api_key)
  prompt = """
    You are a virtual try-on engine.
    Take the clothing item from the second image and realistically fit it onto the person in the first image.
    Maintain the person's body shape, pose, lighting, and skin tone.
    Make sure the garment follows natural wrinkles, shadows, and alignment.
    Produce a realistic full-body try-on result without altering the person’s identity.
    """
  response = client.models.generate_content(
      model="gemini-2.5-flash-image",
      contents=[prompt, person_img, garment_img],
  )

  raw_img = None
  for part in response.parts:
    if part.inline_data is not None:
      raw_img = part.inline_data.data
      break

  if raw_img is None:
    raise RuntimeError("No image returned from Gemini.")
  
  pil_img = Image.open(io.BytesIO(raw_img))
  return pil_img


# -------------------------------
# ❗ Example Usage
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
      "--person",
      help="person img path",
      default="../demo/p1.png"
    )
    parser.add_argument(
      "--garment",
      help="garment img path",
      default="../demo/g1.png"
    )
    args = parser.parse_args()
    
    garment = Image.open(args.garment)
    person = Image.open(args.person)

    result = run_virtual_tryon(person, garment)
    result.save("../demo/result.png")
    print("Virtual Try-On Image Saved: result.png")