from flask import Flask, jsonify, send_from_directory, request
import os
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route("/rot")
def rot():
    chave = request.args.get('chave')
    texto = request.args.get('texto')

    try:
        int(chave)
    except x:
        return ":(", 400

    processo = Popen(f'python rot.py {chave}', shell = True, stdin = PIPE, stdout = PIPE)
    processo.stdin.write(texto.encode('utf-8'))
    out = processo.communicate()[0]
    return out

if __name__ == "__main__":
    app.run(port = 10101)