from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    session,
)
import os, config
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_DB"] = config.MYSQL_DB
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["SECRET_KEY"] = config.HEX_SEC_KEY  # Configurar la clave secreta

mysql = MySQL(app)


@app.route("/")
def index():
    if "email" in session:
        return render_template("index.html", email=session["email"])
    else:
        return render_template("sign.html")


@app.route("/sign", methods=["GET", "POST"])
def sign():
    if "email" in session:
        return render_template("index.html", email=session["email"])
    else:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_email = cur.fetchone()

            if not existing_email:
                # El correo electrónico no está registrado
                email_not_found = True
                return render_template("sign.html", email_not_found=email_not_found)

            cur.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password),
            )

            user = cur.fetchone()
            cur.close()

            if user:
                # Contraseña correcta
                session["email"] = email
                return redirect(url_for("index", user=email))
            else:
                # Contraseña incorrecta
                bad_password = True
                return render_template(
                    "sign.html", bad_password=bad_password, email=email
                )
        return render_template("sign.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "email" in session:
        return render_template("index.html", email=session["email"])
    else:
        if request.method == "POST":
            name = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_email = cur.fetchone()

            cur.execute("SELECT * FROM users WHERE name = %s", (name,))
            existing_user = cur.fetchone()

            if existing_email:
                error_message = "El correo electrónico ya está registrado. Por favor, utiliza otro correo electrónico."
                return render_template("signup.html", error_message=error_message)

            elif existing_user:
                error_message = (
                    "El usuario ya existe. Por favor, elige otro correo electrónico."
                )
                return render_template("signup.html", error_message=error_message)
            else:
                cur.execute(
                    "INSERT INTO users (name,email, password) VALUES (%s, %s, %s)",
                    (name, email, password),
                )
                mysql.connection.commit()
                session["email"] = email
                return redirect(url_for("registro_exitoso"))

        return render_template("signup.html")


@app.route("/Signout")
def Signout():
    email = session.get("email")  # Obtener el valor de 'email' de la sesión
    session.pop(
        "email", None
    )  # Eliminar la clave 'email' de la sesión si está presente
    return render_template("sign.html")


@app.route("/registro_exitoso")
def registro_exitoso():
    return render_template("registro_exitoso.html")


@app.route("/page1/<user>")
def profile(user):
    if "email" in session:
        email = session["email"]
        return render_template("profile.HTML", email=email)
    else:
        return redirect(url_for("sign"))


@app.route("/buscar", methods=["GET"])
def buscar():
    query = request.args.get("query")  # Obtener la consulta de búsqueda de la URL
    if query == "index":
        return redirect(url_for("index"))  # Redirigir a la página 'Index'
    elif query == "signup":
        return redirect(url_for("signup"))  # Redirigir a la página 'signup'
    elif query == "sign":
        return redirect(url_for("signup"))  # Redirigir a la página 'Habilsignupidades'
    else:
        return render_template("404.html", query=query)  # Página no encontrada 404


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(debug=True)
