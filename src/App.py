# author: Emmanuel Jesus Coba Cuevas
from flask import Flask, render_template, request, redirect, url_for
user = ""
app = Flask(__name__) 

usuarios = {
    'u@1': 'c1',
    'u@2': 'c2'
}

@app.route('/')
def index(): 
    return render_template('index.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and usuarios[username] == password:
            return redirect ("/page1/" + user)

        else:
            error_message = "Usuario o contraseña incorrecta"
            return render_template ('login.html', error_message=error_message)
    return render_template('login.html') 

@app.route('/sign',  methods=['GET', 'POST'])
def sign(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in usuarios:
            error_message = "El usuario ya existe. Por favor, elige otro nombre de usuario."
            return render_template ('sign.html', error_message=error_message)
        else:
            usuarios[username] = password
    return render_template('sign.html')  

@app.route('/page1/<user>')
def saludo(user):
    return '<h2>hola '+ user +'</h2>'
app.run(debug=True) 