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
from datetime import datetime
import config
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_DB"] = config.MYSQL_DB
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["SECRET_KEY"] = config.HEX_SEC_KEY  # Configurar la clave secreta
mysql = MySQL(app)


# Index principal
@app.route("/")
def index():
    # Verificar si hay una dirreccion de correo dentro de session
    if "email" in session:
        full_name = (
            f"{session.get('name', '').strip()} {session.get('last_name', '').strip()}"
        )
        print(full_name)
        # Renderizar la plantilla index.html con la dirrecion del correo y la variable
        return render_template(
            "index.html", email=session["email"], full_name=full_name
        )
    else:
        return render_template("index.html")


# Sign
@app.route("/sign", methods=["GET", "POST"])
def sign():
    if "email" in session:

        return render_template("index.html", email=session["email"])
    else:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
            existing_email = cur.fetchone()
            cur.close()
            print(existing_email)

            if not existing_email:
                # El correo electrónico no está registrado
                email_not_found = True
                return render_template(
                    "auth/signin.html", email_not_found=email_not_found
                )
            else:
                # El correo electrónico está registrado

                if existing_email[4] == password:
                    # Contraseña correcta
                    session["email"] = email
                    session["name"] = existing_email[1]
                    session["last_name"] = existing_email[2]
                    return redirect(url_for("index", user=email))
                else:
                    # Contraseña incorrecta
                    bad_password = True
                    return render_template(
                        "auth/signin.html", bad_password=bad_password, email=email
                    )
        return render_template("auth/signin.html")


# Sign-Up
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Verificar si hay una dirreccion de correo dentro de session
    if "email" in session:
        return render_template("index.html", email=session["email"])
    else:
        if request.method == "POST":
            email_found = False
            user_found = False
            lastname_error = False

            name = request.form.get("name")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            password = request.form.get("password")

            aux = lastname.split()
            if len(aux) >= 2:
                apellido_paterno = aux[0]  # El primer elemento es el apellido paterno
                apellido_materno = aux[-1]  # El último elemento es el apellido materno
                print("Apellido paterno:", apellido_paterno)
                print("Apellido materno:", apellido_materno)
            else:
                lastname_error = True

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
            existing_email = cur.fetchone()

            cur.execute(
                "SELECT * FROM employee WHERE name = %s AND last_name = %s",
                (name, lastname),
            )
            existing_user = cur.fetchone()

            # Existe el correo en la base de datos
            if existing_email:
                email_found = True
            # Existe el usuario en la base de datos
            if existing_user:
                user_found = True
            if existing_email or existing_user or lastname_error:
                return render_template(
                    "auth/signup.html",
                    user_found=user_found,
                    email_found=email_found,
                    lastname_error=lastname_error,
                )

            # No hay ningun error
            else:
                # registrar en base de datos
                cur.execute(
                    "INSERT INTO employee (name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                    (name, lastname, email, password),
                )
                mysql.connection.commit()
                return render_template("auth/signin.html", registration_successful=True)

        return render_template("auth/signup.html")


# Sign-Out
@app.route("/Signout")
def Signout():
    if "email" in session:
        email = session.get("email")  # Obtener el valor de 'email' de la sesión
        session.pop(
            "email", None
        )  # Eliminar la clave 'email' de la sesión si está presente
        return render_template("auth/signin.html")
    else:
        return redirect(url_for("sign"))


# Registro exitoso
@app.route("/successful_registration")
def successful_registration():
    registration_successful = request.args.get("registration_successful")
    if registration_successful == "True":
        return render_template("successful_registration.html")
    else:
        return index()


# Apartado perfil
@app.route("/profile")
def profile():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        return render_template(
            "profile.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


# Apartado de cuanta en ajustes
@app.route("/settings/account")
def account():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        return render_template(
            "account.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


# Apartado de seguridad en ajustes
@app.route("/settings/security")
def security():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        return render_template(
            "security.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


# Apartado de borrar cuenta en ajustes
@app.route("/settings/deleteaccount")
def deleteaccount():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()
        return render_template(
            "deleteaccount.html", email=session["email"], user_data=user_data
        )
    else:
        return redirect(url_for("sign"))


# Cambiar contraseña
@app.route("/settings/ChangePassword", methods=["POST"])
def ChangePassword():
    if "email" in session and request.method == "POST":
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
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
                "UPDATE employee SET password = %s WHERE email = %s",
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


# Cambiar Email
@app.route("/settings/ChangeEmail", methods=["POST"])
def ChangeEmail():
    if "email" in session and request.method == "POST":
        email = session["email"]
        newemail = request.form.get("email")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        user_data = cur.fetchone()

        cur.execute("SELECT * FROM employee WHERE email = %s", (newemail,))
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
                "UPDATE employee SET email = %s WHERE email = %s",
                (newemail, email),
            )
            mysql.connection.commit()
            cur.close()
            session["email"] = newemail
            ChangedEmail = True
            return render_template("Change.HTML", ChangedEmail=ChangedEmail)
    return redirect(url_for("sign"))


# Cambiar propiedades
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
        cur.execute("SELECT * FROM employee WHERE email = %s", (email,))
        user_data = cur.fetchone()

        # Verificar si el nuevo nombre ya existe en la base de datos
        cur.execute(
            "SELECT * FROM employee WHERE name = %s AND email != %s", (new_name, email)
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
                "UPDATE employee SET name = %s, phone = %s WHERE email = %s",
                (new_name, new_phone, email),
            )
            mysql.connection.commit()
            cur.close()
            ChangedProfile = True
            return render_template("Change.HTML", ChangedProfile=ChangedProfile)
    else:
        return redirect(url_for("sign"))


# Borrar cuenta
@app.route("/Delete_Account")
def Delete_Account():
    if "email" in session:
        email = session.get("email")  # Obtener el valor de 'email' de la sesión
        # Conectarse a la base de datos y eliminar al usuario
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM employee WHERE email = %s", (email,))
        mysql.connection.commit()
        cur.close()
        session.pop(
            "email", None
        )  # Eliminar la clave 'email' de la sesión si está presente
        return render_template("sign.html")
    else:
        return redirect(url_for("sign"))


# TABLAS
@app.route("/tasks", methods=["GET"])
def tasks():
    if "email" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        cur.close()
        return render_template("Products/add-products.html", tasks=tasks, email=session["email"])
    else:
        return redirect(url_for("sign"))


@app.route("/add_task", methods=["POST"])
def add_task():
    if "email" in session and request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        cantidad = request.form["cantidad"]
        cur = mysql.connection.cursor()
        # Obtener la fecha y hora actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            "INSERT INTO tasks (nombre, cantidad, descripcion, email, fecha) VALUES (%s, %s, %s, %s, %s)",
            (nombre, cantidad, descripcion, session["email"], fecha_actual),
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("tasks"))
    else:
        return redirect(url_for("sign"))


@app.route("/edit_task/<int:id>", methods=["POST"])
def edit_task(id):
    if "email" in session and request.method == "POST":
        cur = mysql.connection.cursor()
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        cantidad = request.form["cantidad"]
        cur.execute(
            "UPDATE tasks SET nombre = %s, cantidad= %s, descripcion = %s  WHERE id = %s",
            (nombre, cantidad, descripcion, id),
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("tasks"))
    else:
        return redirect(url_for("sign"))


@app.route("/delete_task", methods=["POST"])
def delete_task():
    if "email" in session:
        cur = mysql.connection.cursor()
        id = request.form["task_id"]
        print("Valor de id:", id)
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("tasks"))
    else:
        return redirect(url_for("sign"))


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(debug=True, port=9000)
