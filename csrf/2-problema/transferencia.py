from flask import Flask, make_response, render_template, request
app = Flask(__name__)

usuarios = {
    "dumbledore": {"senha": "hogwarts", "saldo": 7000000.00},
    "harry potter": {"senha": "alohomora", "saldo": 1000000.00},
    "hermione": {"senha": "wingardium leviossa", "saldo": 5000.00},
    "snape": {"senha": "sonserina", "saldo": 6000.00},
    "voldemort": {"senha": "avada kedavra", "saldo": 0.50},
    "draco malfoy": {"senha": "fora trouxas", "saldo": 30.00}
}

def achar_usuario(login):
    return usuarios[login] if login in usuarios else None

@app.route("/")
def tela_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    logado = achar_usuario(login)
    if logado is None or logado['senha'] != senha:
        return render_template("login.html")
    return render_template("bem-vindo.html", usuario_atual = login, usuarios = usuarios)

@app.route("/login", methods=["POST"])
def login():
    f = request.form
    if 'login' not in f or 'senha' not in f:
        return ":(", 422
    login = f['login']
    senha = f['senha']
    logado = achar_usuario(login)
    if logado is None or logado['senha'] != senha:
        return render_template("login.html", erro = 'Ops. A senha estava errada.')
    resposta = make_response(render_template("bem-vindo.html", usuario_atual = login, usuarios = usuarios))
    resposta.set_cookie('login', login)
    resposta.set_cookie('senha', senha)
    return resposta

@app.route("/logout", methods=["POST"])
def logout():
    resposta = make_response(render_template("login.html", mensagem = 'Tchau'))
    resposta.set_cookie('login', '')
    resposta.set_cookie('senha', '')
    return resposta

@app.route("/transferir", methods = ["POST"])
def transferir():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    logado = achar_usuario(login)
    if logado is None or logado['senha'] != senha:
        return render_template("login.html", erro = 'Ops. Parece que seu login não é mais válido.')

    f = request.form
    if 'destinatario' not in f or 'valor' not in f:
        return ":(", 422

    destinatario = achar_usuario(request.form['destinatario'])
    valor = float(request.form['valor'])

    if destinatario is None:
        return ":?", 404
    if logado['saldo'] < valor:
        return "Saldo insuficiente", 422
    logado['saldo'] -= valor
    destinatario['saldo'] += valor
    return render_template("bem-vindo.html", usuario_atual = login, usuarios = usuarios)

if __name__ == "__main__":
    app.run(port = 2020)