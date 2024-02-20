# author: Emmanuel Jesus Coba Cuevas
from flask import Flask, render_template, request, redirect, url_for
user = ""
app = Flask(__name__) 

@app.route('/')
def index(): 
    data={
        'titulo':'Página plantilla',
        'mensaje':'Bienvenido al sitio Web ',
        'nombre' : 'Emmanuel Jesus Coba Cuevas'
        }
    return render_template('index.html',data=data)  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (username == 'u' and password == '1'):
            user = username
            error_message = "todo correcto"
            return redirect ("/page1/" + user)

        else:
            error_message = "Usuario o contraseña incorrecta"
            print (error_message)
    return render_template('login.html') 

@app.route('/page1/<user>')
def saludo(user):
    return '<h2>hola '+ user +'</h2>'
app.run(debug=True) 