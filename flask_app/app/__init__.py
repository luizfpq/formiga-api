# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)

from app.routes.users import users
from app.routes.payment_method import payment_method
from app.routes.payment_source import payment_source
from app.routes.expense_category import expense_category
#from app.routes.items import items
from app.routes.transactions import transactions
#from app.routes.categories import categories

app.register_blueprint(users)
app.register_blueprint(payment_method)
app.register_blueprint(payment_source)
app.register_blueprint(expense_category)
app.register_blueprint(transactions)
#app.register_blueprint(categories)
