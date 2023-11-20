from app import app, db
from flasgger import Swagger  # Importe o Swagger

if __name__ == '__main__':
    # Inicialize o Swagger com a configuração da aplicação Flask
    swagger = Swagger(app)

    with app.app_context():
        # Cria as tabelas no banco de dados antes de iniciar o servidor
        db.create_all()

    # Inicie o servidor Flask
    app.run(host='0.0.0.0', debug=True)
