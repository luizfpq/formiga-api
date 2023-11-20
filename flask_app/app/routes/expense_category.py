# app/routes/expense_categories.py

from flask import Blueprint, request,jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from app import db
from app.models import ExpenseCategory

expense_category = Blueprint('expense_category', __name__)

# Rota para criar uma nova Expense Category
@expense_category.route('/expense_category', methods=['POST'])
def create_expense_category():
    data = request.get_json()
    new_category = ExpenseCategory(category_name=data['category_name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'New expense category created successfully'}), 201

# Rota para obter todas as Expense Categories
@expense_category.route('/expense_category', methods=['GET'])
def get_all_expense_categories():
    """
    Obtém todas as categorias de despesa.
    ---
    tags:
      - Expense Category
    responses:
      200:
        description: Retorna todas as categorias de despesa
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID da categoria de despesa
              category_name:
                type: string
                description: Nome da categoria de despesa
      400:
        description: Erro ao buscar as categorias de despesa
    """
    categories = ExpenseCategory.query.all()
    result = [{'id': category.id, 'category_name': category.category_name} for category in categories]
    return jsonify(result), 200

# Rota para obter uma Expense Category específica
@expense_category.route('/expense_category/<int:category_id>', methods=['GET'])
def get_expense_category(category_id):
    category = ExpenseCategory.query.get(category_id)
    if category:
        return jsonify({'id': category.id, 'category_name': category.category_name}), 200
    return jsonify({'message': 'Expense category not found'}), 404

# Rota para atualizar uma Expense Category
@expense_category.route('/expense_category/<int:category_id>', methods=['PUT'])
def update_expense_category(category_id):
    category = ExpenseCategory.query.get(category_id)
    if category:
        data = request.get_json()
        category.category_name = data['category_name']
        db.session.commit()
        return jsonify({'message': 'Expense category updated successfully'}), 200
    return jsonify({'message': 'Expense category not found'}), 404

# Rota para deletar uma Expense Category
@expense_category.route('/expense_category/<int:category_id>', methods=['DELETE'])
def delete_expense_category(category_id):
    category = ExpenseCategory.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Expense category deleted successfully'}), 200
    return jsonify({'message': 'Expense category not found'}), 404