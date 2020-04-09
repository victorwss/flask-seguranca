import sqlite3
from contextlib import closing

criacao_bd = """
CREATE TABLE IF NOT EXISTS usuarios (
    login VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL
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

def rot(chave, texto):
    tabela = {}
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    for a in range(0, 26):
        tabela[alfabeto[a]] = alfabeto[(a + 26 + chave) % 26]
        tabela[alfabeto[a].upper()] = alfabeto[(a + 26 + chave) % 26].upper()
    novo = '';
    for x in texto:
        if x in tabela:
            novo += tabela[x]
        else:
            novo += x
    return novo

def criptografar(texto):
    return rot(8, texto)

def descriptografar(texto):
    return rot(-8, texto)

def conectar():
    return sqlite3.connect("teste.db")

def criar_bd():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(criacao_bd)
        for u in usuarios_iniciais:
            print(f"Login: {u}, senha: {usuarios_iniciais[u]}")
            cur.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (u, criptografar(usuarios_iniciais[u])))
        con.commit()

def inserir_usuario(login, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (login, criptografar(senha)))
        con.commit()

def achar_usuario(login):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT senha FROM usuarios WHERE login = ?", (login, ))
        t = cur.fetchone()
        if t is None: return None
        return {"login": login, "senha": t[0]}

def verificar_login(login, senha):
    u = achar_usuario(login)
    if u == None: return False
    return descriptografar(u['senha']) == senha
    #return u['senha'] == criptografar(senha)

def listar_usuarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT login, senha FROM usuarios")
        r = []
        t = cur.fetchall()
        for u in t:
            r.append({"login": u[0], "senha": u[1]})
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
