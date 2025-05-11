from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import io
import os
from flask_cors import CORS


genai.configure(api_key="AIzaSyDpLr3nlQZ5cCVaCKAd1QXRTEQjkd-ZHpU")

app = Flask(__name__)


CORS(app, origins="*",supports_credentials=True)



@app.route("/caption", methods=["POST"])
def generate_caption():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "No image selected"}), 400

    try:
        image = Image.open(io.BytesIO(image_file.read()))

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            ["Generate very simple one single line caption for the following image. Do not use any other sentence or line since i am using this generated output in my other project", image],
            stream=False,
        )

        caption = response.text.strip()
        return jsonify({"caption": caption})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
