from flask import Flask, request, jsonify
import replicate

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    image_url = data.get("image_url")

    output = replicate.run(
        "sczhou/codeformer:latest",  # or another model you use
        input={"image": image_url}
    )

    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
