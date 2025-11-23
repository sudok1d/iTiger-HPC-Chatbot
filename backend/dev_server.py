from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    return jsonify({"response": f"Local backend received: {data['message']}"})

app.run(port=7860)
