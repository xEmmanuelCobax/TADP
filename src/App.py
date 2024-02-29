# author: Emmanuel Jesus Coba Cuevas
from flask import Flask, render_template, request, redirect, url_for
user = ""
app = Flask(__name__) 

@app.route('/')
def index(): 
    
    return render_template('index.html') 

@app.route('/conocerme')
def conocerme(): 
    
    return render_template('conocerme.html') 

@app.route('/habilidades')
def habilidades(): 
    
    return render_template('habilidades.html') 
"""
@app.route('/')
def index(): 
    
    return render_template('index.html')  
"""
app.run(debug=True) 