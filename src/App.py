# author: Emmanuel Jesus Coba Cuevas
from flask import Flask, render_template 

app = Flask(__name__) 

@app.route('/')
def Hola(): 
    data={
        'titulo':'Página plantilla',
        'mensaje':'Bienvenido al sitio Web ',
        'nombre' : 'Emmanuel Jesus Coba Cuevas'
        }
    return render_template('pagina1.html',data=data) 
app.run(debug=True) 