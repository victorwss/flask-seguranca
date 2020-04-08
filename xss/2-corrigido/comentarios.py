from flask import Flask, request
app = Flask(__name__)

lista_comentarios = []

modelo_html = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Comentários</title>
        <style>
            textarea {
                min-width: 500px;
            }
        </style>
    </head>
    <body>
        <h1>Comentários:</h1>
        XXXX
        <h2>Deixe seu comentário:</h2>
        <form action="./comentarios" method="POST">
            <p><textarea name="texto"></textarea></p>
            <p><button type="submit">Enviar</button></p>
        </form>
    </body>
</html>"""

def mostrar_comentarios():
    html = modelo_html
    if len(lista_comentarios) == 0:
        html = html.replace("XXXX", "<p>Não há nenhum comentário ainda... Escreva o primeiro!</p>")
    else:
        parte = ""
        for comentario in lista_comentarios:
            comentario_ok = comentario.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;").replace('"', "&#34;").replace('"', "&#39;")
            parte += "<p>" + comentario_ok + "</p>"
        html = html.replace("XXXX", parte)
    return html

@app.route("/")
@app.route("/comentarios")
def ler_comentarios():
    return mostrar_comentarios()

@app.route("/comentarios", methods = ["POST"])
def postar_comentario():
    comentario = request.form['texto']
    lista_comentarios.append(comentario)
    return mostrar_comentarios()

if __name__ == "__main__":
    app.run()