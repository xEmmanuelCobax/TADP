# author: Emmanuel Jesus Coba Cuevas
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__) 
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index(): 
    return render_template('index.html') 

@app.route('/conocerme')
def conocerme(): 
    
    return render_template('conocerme.html') 

@app.route('/formacion')
def formacion(): 
    
    return render_template('formacion.html')

@app.route('/habilidades')
def habilidades(): 
    
    return render_template('habilidades.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('query')  # Obtener la consulta de búsqueda de la URL
    if query == 'conocerme':
        return redirect(url_for('conocerme'))  # Redirigir a la página 'Conocerme'
    elif query == 'formacion':
        return redirect(url_for('formacion'))  # Redirigir a la página 'Formacion'
    elif query == 'habilidades':
        return redirect(url_for('habilidades'))  # Redirigir a la página 'Habilidades'
    else:
        return render_template('404.html', query=query)  # Página no encontrada
    

app.run(debug=True) 