# app/routes/payment_method.py

from flask import Blueprint, request,jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from app import db
from app.models import PaymentMethod

payment_method = Blueprint('payment_method', __name__)

# Rota para criar um novo Payment Method
@payment_method.route('/payment_method', methods=['POST'])
def create_payment_method():
    data = request.get_json()
    new_method = PaymentMethod(method_name=data['method_name'])
    db.session.add(new_method)
    db.session.commit()
    return jsonify({'message': 'New payment method created successfully'}), 201

# Rota para obter todos os Payment Methods
@payment_method.route('/payment_method', methods=['GET'])
def get_all_payment_methods():
    """
    Obtém todos os métodos de pagamento.
    ---
    tags:
      - Payment Method
    responses:
      200:
        description: Retorna todos os métodos de pagamento
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID do método de pagamento
              method_name:
                type: string
                description: Nome do método de pagamento
      400:
        description: Erro ao buscar os métodos de pagamento
    """
    methods = PaymentMethod.query.all()
    result = [{'id': method.id, 'method_name': method.method_name} for method in methods]
    return jsonify(result), 200

# Rota para obter um Payment Method específico
@payment_method.route('/payment_method/<int:method_id>', methods=['GET'])
def get_payment_method(method_id):
    method = PaymentMethod.query.get(method_id)
    if method:
        return jsonify({'id': method.id, 'method_name': method.method_name}), 200
    return jsonify({'message': 'Payment method not found'}), 404

# Rota para atualizar um Payment Method
@payment_method.route('/payment_method/<int:method_id>', methods=['PUT'])
def update_payment_method(method_id):
    method = PaymentMethod.query.get(method_id)
    if method:
        data = request.get_json()
        method.method_name = data['method_name']
        db.session.commit()
        return jsonify({'message': 'Payment method updated successfully'}), 200
    return jsonify({'message': 'Payment method not found'}), 404

# Rota para deletar um Payment Method
@payment_method.route('/payment_method/<int:method_id>', methods=['DELETE'])
def delete_payment_method(method_id):
    method = PaymentMethod.query.get(method_id)
    if method:
        db.session.delete(method)
        db.session.commit()
        return jsonify({'message': 'Payment method deleted successfully'}), 200
    return jsonify({'message': 'Payment method not found'}), 404