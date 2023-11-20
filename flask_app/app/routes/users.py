# app/routes/users.py

from flask import Blueprint, request,jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from app import db
from app.models import User
import hashlib
import time

users = Blueprint('users', __name__)

@users.route('/users/signup', methods=['POST'])
def signup():
    """
    Cadastro de usuário.
    ---
    tags:
      - Usuários
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Nome de usuário
      - name: name
        in: formData
        type: string
        required: true
        description: Nome completo do usuário
      - name: email
        in: formData
        type: string
        required: true
        description: Endereço de e-mail do usuário
      - name: password
        in: formData
        type: string
        required: true
        description: Senha do usuário
      - name: role
        in: formData
        type: string
        required: true
        description: Papel do usuário
    responses:
      201:
        description: Usuário cadastrado com sucesso
      400:
        description: Erro no cadastro do usuário
    """
    try:
        data = request.get_json()

        # Verifique se todos os campos necessários estão presentes na requisição
        required_fields = ['username', 'name', 'password', 'email', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # Verifique se o papel (role) é válido
        valid_roles = ['master', 'admin', 'user']
        if data['role'] not in valid_roles:
            return jsonify({'message': 'Invalid role'}), 400

        # Gere um salt usando o timestamp atual
        salt = str(int(time.time()))

        # Concatene a senha com o salt e aplique hash SHA-256
        hashed_password = generate_password(data['password'], salt)

        # Crie e adicione o usuário ao banco de dados
        new_user = User(
            username=data['username'],
            name=data['name'],
            password=hashed_password,
            email=data['email'],
            role=data['role'],
            salt=salt
        )

        db.session.add(new_user)
        db.session.commit()
        # Retorna os dados do usuário recém-criado
        user_data = {
            'id': new_user.id,
            'username': new_user.username,
            'name': new_user.name,
            'email': new_user.email,
            'role': new_user.role
        }
        
        return jsonify(user_data), 201  # 201 significa Created
    except IntegrityError as e:
        # Se ocorrer uma violação de integridade (por exemplo, e-mail duplicado),
        # faça o rollback e retorne uma mensagem de erro
        db.session.rollback()
        return jsonify({'error': 'E-mail em uso.'}), 400  # 400 significa Bad Request

@users.route('/users/login', methods=['POST'])
def login():
    """
    Autenticação de usuário.
    ---
    tags:
      - Usuários
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: Endereço de e-mail do usuário
      - name: password
        in: formData
        type: string
        required: true
        description: Senha do usuário
    responses:
      200:
        description: Autenticação bem-sucedida
      401:
        description: Credenciais inválidas
    """
    # Obtém as credenciais do JSON no corpo da solicitação
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Credenciais incompletas'}), 400

    email = data['email']
    password = data['password']

    # Procura o usuário no banco de dados pelo e-mail
    user = User.query.filter_by(email=email).first()
    print(user)

    if user and check_password(user.password, user.salt, password):
        # Se as credenciais estiverem corretas, cria um token de acesso JWT
        access_token = create_access_token(identity=user.id)

        # Retorna o token no formato JSON
        return jsonify(access_token=access_token), 200

    # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
    return jsonify({'error': 'Credenciais inválidas'}), 401

#cria o hash da senha para transacoes
def generate_password(password, salt):
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

#checa os hashs na autenticacao
def check_password(saved_password, salt, provided_password):
    provided_password = generate_password(provided_password, salt)
    return saved_password == provided_password
    # Use a função de comparação do Flask-WTF (check_password_hash) se preferir
    # return check_password_hash(saved_password, provided_password)


# rota de logout
@users.route('/users/logout', methods=['POST'])
@jwt_required()
def logout():
    # Obtenha a identidade do token JWT
    current_user_id = get_jwt_identity()

    # Lógica de logout aqui, se necessário

    # Remova os cookies relacionados ao JWT
    response = jsonify({'message': 'Logout bem-sucedido'})
    unset_jwt_cookies(response)
    return response, 200


# Exemplo de uma rota protegida que requer autenticação usando JWT
@users.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Obtém a identidade do token JWT
    current_user_id = get_jwt_identity()

    # Retorna a mensagem protegida
    return jsonify(logged_in_as=current_user_id), 200

@users.route('/users/<int:user_id>', methods=['PUT', 'DELETE'])
def edit_user(user_id):
    # Implemente a lógica de edição ou desativação de usuários aqui
    pass