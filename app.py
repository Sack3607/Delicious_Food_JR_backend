from flask import Flask, request, jsonify
from chatbot import chat  # Aquí pones la función de tu chatbot


app = Flask(__name__)
  # Esto permite que cualquier página pueda hacer requests

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensaje = data.get("mensaje")
    if not mensaje:
        return jsonify({"error": "No se recibió mensaje"}), 400

    respuesta = chat(mensaje)  # Tu función que genera la respuesta
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)