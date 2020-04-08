from flask import Flask, render_template, request
app = Flask(__name__)

lista_comentarios = []

@app.route("/")
@app.route("/comentarios")
def ler_comentarios():
    return render_template("comentarios.html", comentarios = lista_comentarios)

@app.route("/comentarios", methods = ["POST"])
def postar_comentario():
    comentario = request.form['texto']
    lista_comentarios.append(comentario)
    return render_template("comentarios.html", comentarios = lista_comentarios)

if __name__ == "__main__":
    app.run()