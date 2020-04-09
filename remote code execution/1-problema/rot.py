from sys import argv

tabela = {}

alfabeto = 'abcdefghijklmnopqrstuvwxyz'

def rot(chave, texto):
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

if __name__ == "__main__":
    chave = int(argv[1])
    texto = ' '.join(argv[2:])
    print(rot(chave, texto))