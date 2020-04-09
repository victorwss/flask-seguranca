from requests import api
import os

arquivo = input("Digite o nome do arquivo: ")
salvar_como = input("Com qual nome você gostaria de salvá-lo? ")

url = f"http://localhost:9090/downloads?arquivo={arquivo}"
print(f"Fazendo o download de {url}")

r = api.get(url)
status = r.status_code

if status != 200:
    print(f"Deu erro {status}. Que triste...")
else:
    with open(os.path.join("baixados", salvar_como), "wb") as f:
        f.write(r.content)
    print("Sucesso! :)")