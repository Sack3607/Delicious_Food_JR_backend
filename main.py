from flask import Flask, send_from_directory


app = Flask(
    __name__,
    static_folder="../frontend",  # toda la carpeta frontend
    static_url_path=""            # sirve directamente desde la raíz
)


@app.route("/")
def home():
    return send_from_directory("../frontend/pages", "index.html")