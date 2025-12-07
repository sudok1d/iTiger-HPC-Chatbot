import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from model import run_vlm  

frontend_folder = os.path.join(os.path.dirname(__file__), "../frontend")
app = Flask(__name__, static_folder=frontend_folder, static_url_path="")
CORS(app)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    file_path = os.path.join(frontend_folder, path)
    if path != "" and os.path.exists(file_path):
        return app.send_static_file(path)
    return app.send_static_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        text = request.form.get("message", "")
        uploaded_image = request.files.get("image")
        image = None
        if uploaded_image:
            try:
                image = Image.open(uploaded_image.stream).convert("RGB")
            except Exception as e:
                return jsonify({"error": f"Error processing image: {e}"}), 400

        reply = run_vlm(text, image)
        return jsonify({"response": reply})
    except Exception as e:
        print("[ERROR] /chat route failed:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
