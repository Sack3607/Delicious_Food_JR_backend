from fastapi import FastAPI
from flask import Flask, request, jsonify
from chatbot import chat  # Aquí pones la función de tu chatbot
from fastapi.middleware.cors import CORSMiddleware


app = Flask(__name__)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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