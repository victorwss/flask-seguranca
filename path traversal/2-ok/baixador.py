from flask import Flask, send_from_directory, request
import os

app = Flask(__name__)

@app.route("/downloads")
def baixar_arquivo():
    arquivo = request.args.get('arquivo')
    print(f"Abrindo o arquivo {arquivo}.")
    try:
        return send_from_directory('arquivos', arquivo)
    except FileNotFoundError as x:
        return f"Não achei o arquivo {arquivo}.", 404

if __name__ == "__main__":
    app.run(port = 9090)