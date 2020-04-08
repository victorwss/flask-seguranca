from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
@app.route("/link-1")
def parte_1():
    a = "<span style='color: blue'>Este conteúdo é uma parte normal da página e deverá aparecer em azul.</span>"
    b = "<span style='color: red'>Este conteúdo não uma parte normal da página e deverá aparecer da forma como está.</span>"
    return render_template("link-1.html", conteudo_1 = a, conteudo_2 = b)

@app.route("/link-2")
def parte_2():
    x = [
        "<span style='color: green'>VERDE 1</span>",
        "<span style='color: green'>VERDE 2</span>",
        "<span style='color: green'>VERDE 3</span>",
        "<span style='color: green'>VERDE 4</span>",
        "<span style='color: green'>VERDE 5</span>",
        "<span style='color: green'>VERDE 6</span>",
        "<span style='color: green'>VERDE 7</span>"
    ]
    y = "<textarea>Isso deveria estar com escaping</textarea>"
    return render_template("link-2.html", nao_deve_passar_por_escaping = x, variavel_que_precisa_de_escaping = y)

if __name__ == "__main__":
    app.run()