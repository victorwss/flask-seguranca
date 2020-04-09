from sys import argv, stdin

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

def ler_tudo():
    t = ""
    for line in stdin:
        t += "\n"
        t += line
    return t[1:]

if __name__ == "__main__":
    chave = int(argv[1])
    print(rot(chave, ler_tudo()))