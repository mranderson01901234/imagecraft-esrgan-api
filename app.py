from flask import Flask, request, jsonify
import base64, subprocess, os
from PIL import Image
import io

app = Flask(__name__)

@app.route("/enhance", methods=["POST"])
def enhance():
    data = request.json
    base64_data = data.get("image_base64", "").split(",")[-1]

    try:
        # Save input image
        with open("input.png", "wb") as f:
            f.write(base64.b64decode(base64_data))

        # Run Real-ESRGAN (placeholder, command must be installed inside container)
        subprocess.run(["realesrgan-ncnn-vulkan", "-i", "input.png", "-o", "output.png", "-n", "realesrgan-x4plus"])

        # Encode output image
        with open("output.png", "rb") as f:
            result_data = base64.b64encode(f.read()).decode("utf-8")
        return jsonify({ "output_base64": "data:image/png;base64," + result_data })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/ping", methods=["GET"])
def ping():
    return "🟢 ImageCraft AI Server is live"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
