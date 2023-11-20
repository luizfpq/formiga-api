# app/routes/payment_method.py

from flask import Blueprint, request,jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from app import db
from app.models import Transaction

transactions = Blueprint('transactions', __name__)

# Rotas CRUD para Transaction
@transactions.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Obtém todas as transações.
    ---
    tags:
      - Transactions
    responses:
      200:
        description: Retorna todas as transações
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID da transação
              date:
                type: string
                format: date-time
                description: Data da transação (no formato YYYY-MM-DD HH:MM:SS)
              value:
                type: float
                description: Valor da transação
              description:
                type: string
                description: Descrição da transação
              type:
                type: string
                description: Tipo da transação (Credit ou Debit)
              installments:
                type: integer
                description: Número de parcelas
              planned:
                type: boolean
                description: Indica se a transação é planejada
              status:
                type: boolean
                description: Status da transação
              expense_category_id:
                type: integer
                description: ID da categoria de despesa
              payment_method_id:
                type: integer
                description: ID do método de pagamento
              payment_source_id:
                type: integer
                description: ID da fonte de pagamento
      400:
        description: Erro ao buscar as transações
    """
    transactions = Transaction.query.all()
    return jsonify([{
        'id': transaction.id,
        'date': transaction.date.strftime('%Y-%m-%d %H:%M:%S'),
        'value': transaction.value,
        'description': transaction.description,
        'type': 'Credit' if transaction.type else 'Debit',
        'installments': transaction.installments,
        'planned': bool(transaction.planned),
        'status': bool(transaction.status),
        'expense_category_id': transaction.expense_category_id,
        'payment_method_id': transaction.payment_method_id,
        'payment_source_id': transaction.payment_source_id
    } for transaction in transactions])

@transactions.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return jsonify({
        'id': transaction.id,
        'date': transaction.date.strftime('%Y-%m-%d %H:%M:%S'),
        'value': transaction.value,
        'description': transaction.description,
        'type': 'Credit' if transaction.type else 'Debit',
        'installments': transaction.installments,
        'planned': bool(transaction.planned),
        'status': bool(transaction.status),
        'expense_category_id': transaction.expense_category_id,
        'payment_method_id': transaction.payment_method_id,
        'payment_source_id': transaction.payment_source_id
    })

@transactions.route('/transactions', methods=['POST'])
def create_transaction():
    """
    Cria uma nova transação.
    ---
    tags:
      - Transactions
    parameters:
      - name: transaction_data
        in: body
        required: true
        description: Dados da nova transação
        schema:
          type: object
          properties:
            date:
              type: string
              format: date-time
              description: Data da transação (no formato YYYY-MM-DD HH:MM:SS)
            value:
              type: float
              description: Valor da transação
            description:
              type: string
              description: Descrição da transação
            type:
              type: string
              description: Tipo da transação (Credit ou Debit)
            installments:
              type: integer
              description: Número de parcelas
            planned:
              type: boolean
              description: Indica se a transação é planejada
            status:
              type: boolean
              description: Status da transação
            expense_category_id:
              type: integer
              description: ID da categoria de despesa
            payment_method_id:
              type: integer
              description: ID do método de pagamento
            payment_source_id:
              type: integer
              description: ID da fonte de pagamento
    responses:
      201:
        description: Nova transação criada com sucesso
      400:
        description: Erro ao criar a transação
    """
    data = request.get_json()
    new_transaction = Transaction(
        date=data['date'],
        value=data['value'],
        description=data['description'],
        type=data['type'],
        installments=data['installments'],
        planned=data['planned'],
        status=data['status'],
        expense_category_id=data['expense_category_id'],
        payment_method_id=data['payment_method_id'],
        payment_source_id=data['payment_source_id']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction created successfully'})

@transactions.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    data = request.get_json()
    transaction = Transaction.query.get_or_404(id)
    transaction.date = data['date']
    transaction.value = data['value']
    transaction.description = data['description']
    transaction.type = data['type']
    transaction.installments = data['installments']
    transaction.planned = data['planned']
    transaction.status = data['status']
    transaction.expense_category_id = data['expense_category_id']
    transaction.payment_method_id = data['payment_method_id']
    transaction.payment_source_id = data['payment_source_id']
    db.session.commit()
    return jsonify({'message': 'Transaction updated successfully'})

@transactions.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully'})