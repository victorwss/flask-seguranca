from flask import Flask, jsonify, send_from_directory, request
import os
from subprocess import Popen, PIPE

app = Flask(__name__)

def solucao_gambiarra(texto):
    x = ""
    for a in texto:
        x += "^" + a
    return x

@app.route("/rot")
def rot():
    chave = request.args.get('chave')
    texto = request.args.get('texto')

    try:
        int(chave)
    except x:
        return ":(", 400
    
    out = Popen(f'python rot.py {chave} {solucao_gambiarra(texto)}', shell = True, stdout = PIPE).communicate()[0]
    return out

if __name__ == "__main__":
    app.run(port = 10101)