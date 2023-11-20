from flask import render_template, jsonify
from app import app

@app.route('/')
def index():
    return render_template('index.html')
    #return jsonify({'error': 'Rota não permitida - HTTP 403.'}), 403  # 403 significa Forbidden
@app.route('/enunciado')
def enunciado():
    return render_template('enunciado.html')