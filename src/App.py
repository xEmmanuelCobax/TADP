from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
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

# index principal
@app.route("/")
def index():
    if "email" in session:
        logged_in = True
        return render_template(
            "index.html", email=session["email"], logged_in=logged_in
        )
    else:
        return render_template("index.html")

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
            cur.close()
            print(existing_email)

            if not existing_email:
                # El correo electrónico no está registrado
                email_not_found = True
                return render_template("sign.html", email_not_found=email_not_found)
            else:
                # El correo electrónico está registrado

                if existing_email[3] == password:
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
                email_found = True
                error_message = "The email is already registered."
                return render_template(
                    "signup.html", email_found=email_found, error_message=error_message
                )

            elif existing_user:
                user_found = True
                error_message = "User already exists. Please choose another email."
                return render_template(
                    "signup.html", user_found=user_found, error_message=error_message
                )
            else:
                # registrar en base de datos
                cur.execute( 
                    "INSERT INTO users (name,email, password) VALUES (%s, %s, %s)",
                    (name, email, password),
                )
                mysql.connection.commit() 
                session["email"] = email
                return redirect(
                    url_for("successful_registration", registration_successful=True)
                )

        return render_template("signup.html")


@app.route("/Signout")
def Signout():
    if "email" in session:
        email = session.get("email")  # Obtener el valor de 'email' de la sesión
        session.pop(
            "email", None
        )  # Eliminar la clave 'email' de la sesión si está presente
        return render_template("sign.html")
    else:
        return redirect(url_for("sign"))


@app.route("/successful_registration")
def successful_registration():
    registration_successful = request.args.get("registration_successful")
    if registration_successful == "True":
        return render_template("successful_registration.html")
    else:
        return index()


@app.route("/profile")
def profile():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        print(user_data[1])
        print(user_data[2])
        return render_template(
            "profile.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


@app.route("/settings/account")
def account():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        print(user_data[1])  # USERNAME
        print(user_data[2])  # EMAIL
        print(user_data[3])  # PASSWORD
        return render_template(
            "account.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


@app.route("/settings/security")
def security():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        return render_template(
            "security.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


@app.route("/settings/deleteaccount")
def deleteaccount():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        return render_template(
            "deleteaccount.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


@app.route("/settings/ChangePassword", methods=["POST"])
def ChangePassword():
    if "email" in session and request.method == "POST":
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()

        password = request.form.get("inputPasswordCurrent")
        new_password = request.form.get("inputPasswordNew")
        new_password2 = request.form.get("inputPasswordNew2")

        if (
            user_data
            and user_data[3] == password
            and new_password == new_password2
            and new_password
        ):
            cur.execute(
                "UPDATE users SET password = %s WHERE email = %s",
                (new_password, email),
            )
            mysql.connection.commit()
            cur.close()
            ChangedPassword = True
            return render_template("Change.HTML", ChangedPassword=ChangedPassword)
        elif user_data[3] != password:
            user_data = (user_data,)
            IncorrectPassword = True
            error_message = "The password is incorrect"
            return render_template(
                "security.html",
                email=session["email"],
                user_data=user_data,
                IncorrectPassword=IncorrectPassword,
                error_message=error_message,
            )
        elif not new_password:
            PasswordNone = True
            error_message = "The new password box is empty."
            return render_template(
                "security.html",
                email=session["email"],
                user_data=user_data,
                PasswordNone=PasswordNone,
                error_message=error_message,
            )
        else:
            IncorrectConfirmation = True
            error_message = "The confirmation is incorrect, please try again"
            return render_template(
                "security.html",
                email=session["email"],
                user_data=user_data,
                IncorrectConfirmation=IncorrectConfirmation,
                error_message=error_message,
            )
    else:
        return redirect(url_for("sign"))


@app.route("/settings/ChangeEmail", methods=["POST"])
def ChangeEmail():
    if "email" in session and request.method == "POST":
        email = session["email"]
        newemail = request.form.get("email")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()

        cur.execute("SELECT * FROM users WHERE email = %s", (newemail,))
        existing_email = cur.fetchone()
        cur.close()

        print(existing_email)
        if existing_email:
            email_found = True
            error_message = "The email is already registered."
            return render_template(
                "security.html",
                email=session["email"],
                user_data=user_data,
                email_found=email_found,
                error_message=error_message,
            )
        else:
            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE users SET email = %s WHERE email = %s",
                (newemail, email),
            )
            mysql.connection.commit()
            cur.close()
            session["email"] = newemail
            ChangedEmail = True
            return render_template("Change.HTML", ChangedEmail=ChangedEmail)
    return redirect(url_for("sign"))


from flask import flash


@app.route("/settings/ChangeProfile", methods=["POST"])
def ChangeProfile():
    if "email" in session and request.method == "POST":
        email = session["email"]
        new_name = request.form.get("inputUsername")
        new_phone = request.form.get("inputPhone")
        if not new_name:
            new_name = 0

        cur = mysql.connection.cursor()
        # Encontrar los datos del usuario en la base de datos
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()

        # Verificar si el nuevo nombre ya existe en la base de datos
        cur.execute(
            "SELECT * FROM users WHERE name = %s AND email != %s", (new_name, email)
        )
        existing_user = cur.fetchone()

        if existing_user:
            user_found = True
            error_message = "User already exists. Please choose another email."
            return render_template(
                "account.html",
                email=session["email"],
                user_data=user_data,
                user_found=user_found,
                error_message=error_message,
                new_name=new_name,
            )  # Redirigir a la página de configuración
        else:
            # Actualizar el perfil si no se encuentra otro usuario con el mismo nombre
            cur.execute(
                "UPDATE users SET name = %s, phone = %s WHERE email = %s",
                (new_name, new_phone, email),
            )
            mysql.connection.commit()
            cur.close()
            ChangedProfile = True
            return render_template("Change.HTML", ChangedProfile=ChangedProfile)
    else:
        return redirect(url_for("sign"))


@app.route("/Delete_Account")
def Delete_Account():
    if "email" in session:
        email = session.get("email")  # Obtener el valor de 'email' de la sesión
        # Conectarse a la base de datos y eliminar al usuario
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE email = %s", (email,))
        mysql.connection.commit()
        cur.close()
        session.pop(
            "email", None
        )  # Eliminar la clave 'email' de la sesión si está presente
        return render_template("sign.html")
    else:
        return redirect(url_for("sign"))


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(debug=True, port=9000)
