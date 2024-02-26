# author: Emmanuel Jesus Coba Cuevas
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

try:
    with open('usuarios.json', 'r') as file:
        usuarios = json.load(file)
except FileNotFoundError:
    usuarios = {}

user = ""
app = Flask(__name__) 

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index(): 
    return render_template('index.html')  

@app.route('/prueba')
def prueba(): 
    return render_template('bc.html')  
#Registarse
@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and usuarios[username] == password:
            return redirect (url_for('saludo', user=username))

        else:
            error_message = "Usuario o contraseña incorrecta"
            return render_template ('sign.html', error_message=error_message)
    return render_template('sign.html') 
#Acceder
@app.route('/signup',  methods=['GET', 'POST'])
def signup(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        if username in usuarios:
            error_message = "El usuario ya existe. Por favor, elige otro nombre de usuario."
            return render_template ('signup.html', error_message=error_message)
        else:
            usuarios[username] = password
    return render_template('signup.html')  

@app.route('/page1/<user>')
def saludo(user):
    return '<h2>hola '+ user +'</h2>'
app.run(debug=True) 

if __name__ == '__main__':
    app.run(debug=True)