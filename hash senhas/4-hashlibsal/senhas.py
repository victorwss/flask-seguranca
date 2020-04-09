import sqlite3
from contextlib import closing
import hashlib

criacao_bd = """
CREATE TABLE IF NOT EXISTS usuarios (
    login VARCHAR(100) NOT NULL,
    hash VARCHAR(100) NOT NULL
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

def string_random():
    import random
    import string
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))

def criar_hash(senha):
    sal = string_random()
    return sal + hashlib.sha3_224((sal + senha).encode('utf-8')).hexdigest()

def comparar_hash(senha, hash):
    sal = hash[0:10]
    return sal + hashlib.sha3_224((sal + senha).encode('utf-8')).hexdigest() == hash

def conectar():
    return sqlite3.connect("teste.db")

def criar_bd():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(criacao_bd)
        for u in usuarios_iniciais:
            print(f"Login: {u}, senha: {usuarios_iniciais[u]}")
            cur.execute("INSERT INTO usuarios (login, hash) VALUES (?, ?)", (u, criar_hash(usuarios_iniciais[u])))
        con.commit()

def inserir_usuario(login, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO usuarios (login, hash) VALUES (?, ?)", (login, criar_hash(senha)))
        con.commit()

def achar_usuario(login):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT hash FROM usuarios WHERE login = ?", (login, ))
        t = cur.fetchone()
        if t is None: return None
        return {"login": login, "hash": t[0]}

def verificar_login(login, senha):
    u = achar_usuario(login)
    if u == None: return False
    return comparar_hash(senha, u['hash'])

def listar_usuarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT login, hash FROM usuarios")
        r = []
        t = cur.fetchall()
        for u in t:
            r.append({"login": u[0], "hash": u[1]})
        return r

def mostrar_usuarios():
    usuarios = listar_usuarios()
    for u in usuarios:
        print(u)

def logar():
    login = input("Digite o login: ")
    senha = input("Digite a senha: ")
    if verificar_login(login, senha):
        print("Senha correta.")
    else:
        print("Senha errada.")

def cadastrar_usuario():
    login = input("Digite o login: ")
    senha = input("Digite a senha: ")
    inserir_usuario(login, senha)

instrucoes = """
Digite A para popular o banco de dados.
Digite B para cadastrar um usuário.
Digite C para efetuar o login.
Digite D para listar os usuários.
Digite X para sair.
"""

sair = False
while not sair:
    print(instrucoes)
    acao = input("O que você deseja fazer? ")
    if acao in ['a', 'A']:
        criar_bd()
    elif acao in ['b', 'B']:
        cadastrar_usuario()
    elif acao in ['c', 'C']:
        logar()
    elif acao in ['d', 'D']:
        mostrar_usuarios()
    elif acao in ['x', 'X']:
        sair = True
