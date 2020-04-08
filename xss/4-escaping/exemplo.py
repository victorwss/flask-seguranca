from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
@app.route("/link-1")
def parte_1():
    a = "<p style='color: red'>Este conteúdo é uma parte normal da página e deverá aparecer em vermelho.</p>"
    b = "<p style='color: red'>Este conteúdo não uma parte normal da página e deverá aparecer da forma como está.</p>"
    return render_template("link-1.html", conteudo_1 = a, conteudo_2 = b)

if __name__ == "__main__":
    app.run()