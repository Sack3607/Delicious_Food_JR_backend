from fastapi import FastAPI
from pydantic import BaseModel
import requests
from lector import cargar_conocimiento
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY = "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"

conocimiento = cargar_conocimiento()


class Pregunta(BaseModel):
    mensaje: str


@app.post("/chat")
def chat(data: Pregunta):

    pregunta_usuario = data.mensaje

    prompt = f"""
Responde solo usando la siguiente información.

Información:
{conocimiento}

Pregunta:
{pregunta_usuario}
"""

    respuesta = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "Responde solo con la información dada."},
                {"role": "user", "content": prompt}
            ]
        }
    )
    print("RESPUESTA COMPLETA API:")
    print(respuesta.text)
    data = respuesta.json()

    return {
        "respuesta": data["choices"][0]["message"]["content"]
    }