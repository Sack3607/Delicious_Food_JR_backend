from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from lector import cargar_conocimiento
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------
# Inicialización del servidor
# -------------------------------
app = FastAPI(title="Chatbot API")

# -------------------------------
# Configuración de CORS
# -------------------------------
# Reemplaza "https://tu-pagina-web.com" con el dominio de tu web
origins = [
    "https://delicious-food-jr.onrender.com",  # Dominio real de tu web
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Solo los dominios listados
    allow_credentials=False,
    allow_methods=["*"],         # Permite GET, POST, etc.
    allow_headers=["*"]          # Permite cabeceras como Content-Type
)

# -------------------------------
# Configuración del chatbot
# -------------------------------
API_KEY = "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"
conocimiento = cargar_conocimiento()  # Carga la info desde lector.py

class Pregunta(BaseModel):
    mensaje: str

# -------------------------------
# Endpoint principal
# -------------------------------
@app.post("/chat")
def chat(data: Pregunta):
    pregunta_usuario = data.mensaje.strip()

    if not pregunta_usuario:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")

    prompt = f"""
Responde solo usando la siguiente información.

Información:
{conocimiento}

Pregunta:
{pregunta_usuario}
"""

    try:
        respuesta_api = requests.post(
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
            },
            timeout=15
        )
        respuesta_api.raise_for_status()
        data_api = respuesta_api.json()

        print("RESPUESTA GROQ:", data_api)

        try:
            respuesta_texto = data_api["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            respuesta_texto = "⚠️ No se pudo generar la respuesta."

    except requests.exceptions.RequestException as e:
        print("ERROR AL LLAMAR LA API DE GROQ:", e)
        raise HTTPException(status_code=500, detail="Error al procesar la solicitud en la API externa.")
    except (KeyError, IndexError) as e:
        print("ERROR EN LA RESPUESTA DE LA API:", e)
        raise HTTPException(status_code=500, detail="Respuesta inesperada de la API externa.")
    print(data)
    return {"respuesta": respuesta_texto}

# -------------------------------
# Ruta de prueba
# -------------------------------
@app.get("/")
def root():
    return {"mensaje": "El backend del chatbot está funcionando."}