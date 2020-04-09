from flask import Flask, send_file, request
import os

app = Flask(__name__)

@app.route("/downloads")
def baixar_arquivo():
    arquivo = request.args.get('arquivo')
    caminho = os.path.join(app.root_path, 'arquivos', arquivo)
    print(f"Abrindo o arquivo {caminho}.")
    try:
        return send_file(caminho)
    except FileNotFoundError as x:
        return f"Não achei o arquivo {arquivo}.", 404

if __name__ == "__main__":
    app.run(port = 9090)