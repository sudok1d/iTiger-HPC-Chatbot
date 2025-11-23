from flask import Flask, request, jsonify
from model import run_vlm

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    reply = run_vlm(user_msg)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
