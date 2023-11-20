# app/routes/payment_source.py

from flask import Blueprint, request,jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from app import db
from app.models import PaymentSource

payment_source = Blueprint('payment_source', __name__)

# Rota para criar um novo Payment source
@payment_source.route('/payment_source', methods=['POST'])
def create_payment_source():
    """
    Cria um novo Payment source.
    ---
    tags:
      - Payment Sources
    parameters:
      - name: source_name
        in: body
        type: string
        required: true
        description: Nome do novo Payment source
        schema:
          type: object
          properties:
            source_name:
              type: string
    responses:
      201:
        description: New payment source created successfully
      400:
        description: Invalid or missing parameter
      409:
        description: Payment source already exists
        
    """
    data = request.get_json()
    if 'source_name' not in data or not isinstance(data['source_name'], str):
        return jsonify({'error': 'Invalid or missing source_name parameter'}), 400

    try:
        new_source = PaymentSource(source_name=data['source_name'])
        db.session.add(new_source)
        db.session.commit()
        return jsonify({'message': 'New payment source created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Payment source already exists'}), 409

# Rota para obter todos os Payment sources
@payment_source.route('/payment_source', methods=['GET'])
def get_all_payment_sources():
    """
    Obtém todas as fontes de pagamento.
    ---
    tags:
      - Payment Sources
    responses:
      200:
        description: Retorna todas as fontes de pagamento
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID da fonte de pagamento
              source_name:
                type: string
                description: Nome da fonte de pagamento
      400:
        description: Erro ao buscar as fontes de pagamento
    """
    sources = PaymentSource.query.all()
    result = [{'id': source.id, 'source_name': source.source_name} for source in sources]
    return jsonify(result), 200

# Rota para obter um Payment source específico
@payment_source.route('/payment_source/<int:source_id>', methods=['GET'])
def get_payment_source(source_id):
    source = PaymentSource.query.get(source_id)
    if source:
        return jsonify({'id': source.id, 'source_name': source.source_name}), 200
    return jsonify({'message': 'Payment source not found'}), 404

# Rota para atualizar um Payment source
@payment_source.route('/payment_source/<int:source_id>', methods=['PUT'])
def update_payment_source(source_id):
    source = PaymentSource.query.get(source_id)
    if source:
        data = request.get_json()
        source.source_name = data['source_name']
        db.session.commit()
        return jsonify({'message': 'Payment source updated successfully'}), 200
    return jsonify({'message': 'Payment source not found'}), 404

# Rota para deletar um Payment source
@payment_source.route('/payment_source/<int:source_id>', methods=['DELETE'])
def delete_payment_source(source_id):
    source = PaymentSource.query.get(source_id)
    if source:
        db.session.delete(source)
        db.session.commit()
        return jsonify({'message': 'Payment source deleted successfully'}), 200
    return jsonify({'message': 'Payment source not found'}), 404