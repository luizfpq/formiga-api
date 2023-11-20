# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

jwt = JWTManager(app)

from app.routes.users import users
#from app.routes.items import items
#from app.routes.transactions import transactions
#from app.routes.categories import categories

app.register_blueprint(users)
#app.register_blueprint(items)
#app.register_blueprint(transactions)
#app.register_blueprint(categories)
