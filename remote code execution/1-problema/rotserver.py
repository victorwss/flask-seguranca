from flask import Flask, jsonify, send_from_directory, request
import os
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route("/rot")
def rot():
    chave = request.args.get('chave')
    texto = request.args.get('texto')
    out = Popen(f'python rot.py {chave} {texto}', shell = True, stdout = PIPE).communicate()[0]
    return out

if __name__ == "__main__":
    app.run(port = 10101)