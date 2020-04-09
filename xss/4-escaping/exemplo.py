from flask import Flask, render_template, request
app = Flask(__name__)

bemvindo = """
Seja bem-vindo ao <span style='color: blue; font-weight: bold;'>nosso site</span>.
Esta é uma mensagem que é importante ser exibida com a formatação HTML preservada.
"""

ataque = """
Isto daqui é um comentário de um feito por um usuário mal-intencionado
tentando fazer um <span style='color: red; font-weight: bold;'>XSS</span>.
"""

@app.route("/")
@app.route("/link-1")
def parte_1():
    return render_template("link-1.html", conteudo_1 = bemvindo, conteudo_2 = ataque)

@app.route("/link-2")
def parte_2():
    x = [
        "<span style='color: green'>Não deveria ter escaping 1</span>",
        "<span style='color: green'>Não deveria ter escaping 2</span>",
        "<span style='color: green'>Não deveria ter escaping 3</span>",
        "<span style='color: green'>Não deveria ter escaping 4</span>",
        "<span style='color: green'>Não deveria ter escaping 5</span>",
        "<span style='color: green'>Não deveria ter escaping 6</span>",
        "<span style='color: green'>Não deveria ter escaping 7</span>"
    ]
    y = "<textarea>Isso deveria estar com escaping</textarea>"
    return render_template("link-2.html", nao_deve_passar_por_escaping = x, variavel_que_precisa_de_escaping = y)

if __name__ == "__main__":
    app.run()