from requests import api
import os

def script():
    chave = input("Digite a chave: ")
    texto = input("Digite o texto: ")

    url = f"http://localhost:10101/rot"

    r = api.get(url, params = {"chave": chave, "texto": texto})
    status = r.status_code

    if status != 200:
        print(f"Deu erro {status}. Que triste...")
    else:
        print(r.text)

script()