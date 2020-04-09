import sqlite3
from contextlib import closing
from flask import Flask, make_response, render_template, request

app = Flask(__name__)

criacao_bd = """
CREATE TABLE IF NOT EXISTS usuarios (
    login VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    saldo REAL NOT NULL
);
"""

usuarios_iniciais = {
    "dumbledore": "hogwarts",
    "harry potter": "alohomora",
    "hermione": "wingardium leviossa",
    "snape": "sonserina",
    "voldemort": "avada kedavra",
    "draco malfoy": "fora trouxas",
    "rony": "alohomora"
}

def conectar():
    return sqlite3.connect("banco.db")

def criar_bd():
    try:
        import os
        os.remove("banco.db")
    except FileNotFoundError as x:
        pass
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(criacao_bd)
        for u in usuarios_iniciais:
            cur.execute("INSERT INTO usuarios (login, senha, saldo) VALUES (?, ?, ?)", (u, usuarios_iniciais[u], 5000))
        con.commit()

def achar_usuario(login):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT login, senha, saldo FROM usuarios WHERE login = ? ", (login, ))
        t = cur.fetchone()
        if t is None: return None
        return {"login": t[0], "senha": t[1], "saldo": t[2]}

def login_usuario(login, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT login, senha, saldo FROM usuarios WHERE login = ? and senha = ?", (login, senha))
        t = cur.fetchone()
        if t is None: return None
        return {"login": t[0], "senha": t[1], "saldo": t[2]}

def transferir_valor(de, para, valor):
    sql_a = "UPDATE usuarios SET saldo = saldo - ? WHERE login = ?"
    sql_b = "UPDATE usuarios SET saldo = saldo + ? WHERE login = ?"

    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(sql_a, (valor, de))
        cur.execute(sql_b, (valor, para))
        con.commit()

def listar_usuarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT login, saldo FROM usuarios")
        t = []
        for c in cur.fetchall():
            t.append({"login": c[0], "saldo": c[1]})
        return t

@app.route("/")
def tela_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    logado = login_usuario(login, senha)
    if logado is None:
        return render_template("login.html")
    return render_template("bem-vindo.html", usuario_atual = login, usuarios = listar_usuarios())

@app.route("/login", methods=["POST"])
def login():
    f = request.form
    if 'login' not in f or 'senha' not in f:
        return ":(", 422
    login = f['login']
    senha = f['senha']
    logado = login_usuario(login, senha)
    if logado is None:
        return render_template("login.html", erro = 'Ops. A senha estava errada.')
    resposta = make_response(render_template("bem-vindo.html", usuario_atual = login, usuarios = listar_usuarios()))
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
    logado = login_usuario(login, senha)
    if logado is None:
        return render_template("login.html", erro = 'Ops. Parece que seu login não é mais válido.')

    f = request.form
    if 'destinatario' not in f or 'valor' not in f:
        return ":(", 422

    para = request.form['destinatario']
    valor = request.form['valor']

    if login == para:
        return "Não pode mandar para você mesmo", 422

    if logado['saldo'] < float(valor):
        return "Saldo insuficiente", 422

    transferir_valor(login, para, valor)
    return render_template("bem-vindo.html", usuario_atual = login, usuarios = listar_usuarios())

if __name__ == "__main__":
    criar_bd()
    app.run(port = 2020, host = "127.0.0.101")