# app/routes/payment_method.py

from flask import Blueprint, request,jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text  # Importe a função text do SQLAlchemy
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

@transactions.route('/transactions/total', methods=['GET'])
def get_transaction_type():
    # Consulta à view no banco de dados
    query = text("SELECT * FROM transaction_type_view")  # Sua consulta SQL usando text

    # Execute a consulta
    result = db.session.execute(query)

     # Calcule o total_value a partir dos valores de crédito e débito
    final_value = 0
    transaction_types = []
    
    for row in result:
        if row.transaction_type == "Crédito":
          final_value += row.total_value
          credit_value = row.total_value
        elif row.transaction_type == "Débito":
          final_value -= row.total_value
          debit_value  = row.total_value

      
    transaction_types.append({
        'credit_value': round(credit_value, 2),
        'debit_value' : round(debit_value, 2),
        'final_value' : round(final_value, 2)
    })

    # Retorne os dados como JSON
    return jsonify(transaction_types)


@transactions.route('/transactions/expense_category_totals', methods=['GET'])
def get_transaction_category_totals():
    # Consulta à view no banco de dados
    query = text("SELECT * FROM expense_category_totals")  # Sua consulta SQL usando text

    # Execute a consulta
    result = db.session.execute(query)

    # Transforme o resultado em um dicionário para jsonify
    totals = [
        {'category_id': row.category_id, 'category_name': row.category_name, 'total_value': round(row.total_value, 2)}
        for row in result
    ]
    
    # Retorne os dados como JSON
    return jsonify(totals)

@transactions.route('/transactions/financial_summary', methods=['GET'])
def get_financial_summary():
    # Consulta à view no banco de dados
    query = text("SELECT * FROM financial_summary")  # Sua consulta SQL usando text

    # Execute a consulta
    result = db.session.execute(query)

    # Transforme o resultado em um dicionário para jsonify
    totals = [
        {
            'planned_income': round(row.planned_income, 2),
            'realized_income': round(row.realized_income, 2),
            'planned_expenses': round(row.planned_expenses, 2),
            'realized_expenses': round(row.realized_expenses, 2),
            'planned_balance': round(row.planned_balance, 2),
            'realized_balance': round(row.realized_balance, 2),
            'income_percentage': round(row.income_percentage, 2),
            'expense_percentage': round(row.expense_percentage, 2)
        }
        for row in result
    ]

    
    # Retorne os dados como JSON
    return jsonify(totals)

@transactions.route('/transactions/payment_sources_totals', methods=['GET'])
def get_payment_sources_totals():
    # Consulta à view no banco de dados
    query = text("SELECT * FROM payment_sources_totals")  # Sua consulta SQL usando text

    # Execute a consulta
    result = db.session.execute(query)

    # Transforme o resultado em um dicionário para jsonify
    totals = [
        {
            'source_id': row.source_id,
            'source_name': row.source_name,
            'total_value': round(row.total_value, 2)
        }
        for row in result
    ]

    
    # Retorne os dados como JSON
    return jsonify(totals)

@transactions.route('/transactions/payment_method_totals', methods=['GET'])
def get_payment_method_totals():
    # Consulta à view no banco de dados
    query = text("SELECT * FROM payment_method_totals")  # Sua consulta SQL usando text

    # Execute a consulta
    result = db.session.execute(query)

    # Transforme o resultado em um dicionário para jsonify
    totals = [
        {
            'mothod_id': row.method_id,
            'method_name': row.method_name,
            'total_value': round(row.total_value, 2)
        }
        for row in result
    ]

    
    # Retorne os dados como JSON
    return jsonify(totals)