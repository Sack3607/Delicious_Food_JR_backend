import requests
from bs4 import BeautifulSoup

url = "https://blog-flask-11zv.onrender.com/#comentario"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Buscar solo el contenido principal
articulo = soup.find("article") or soup.find("main") or soup.body

texto = articulo.get_text(separator="\n", strip=True)

with open("contenido2.txt", "w", encoding="utf-8") as f:
    f.write(texto)

print("Contenido principal guardado")