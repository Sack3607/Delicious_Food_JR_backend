
from pathlib import Path

def cargar_conocimiento():
    ruta = Path(__file__).parent / "datos.txt"  # busca dentro de la misma carpeta que lector.py
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()