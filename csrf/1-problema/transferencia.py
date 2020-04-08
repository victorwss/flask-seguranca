from flask import Flask, render_template, request
app = Flask(__name__)

lista_comentarios = []

usuarios = [
    {"login": "dumbledore", "senha": "hogwarts", "saldo": 1000000.00},
    {"login": "harry potter", "senha": "alohomora", "saldo": 1000000.00},
    {"login": "hermione", "senha": "wingardium leviossa", "saldo": 5000.00},
    {"login": "voldemort", "senha": "avada kedavra", "saldo": 0.50}
]

def achar_usuario(login, senha):
    for u in usuarios:
        if u["login"] == login and u["senha"] == senha:
            return u
    return None

@app.route("/")
def tela_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    logado = achar_usuario(login, senha)
    if logado is None:
        return render_template("login.html", senha_errada = False)
    return render_template("bem-vindo.html", usuario = logado)

@app.route("/login", methods=["POST"])
def login():
    f = request.form
    if 'login' not in f or 'senha' not in f: return ":(", 422
    login = f['login']
    senha = f['senha']
    logado = achar_usuario(usuario, senha)
    if logado == None:
        return render_template("login.html", senha_errada = True)
    resposta = render_template("bem-vindo.html", comentarios = lista_comentarios)
    resposta.set_cookie('login', login)
    resposta.set_cookie('senha', senha)
    return resposta

@app.route("/transferir/<de>/<para>/<float:valor>", methods = ["POST"])
def transferir(de, para, valor):
    pass

if __name__ == "__main__":
    app.run()