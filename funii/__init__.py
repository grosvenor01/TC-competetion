from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fun.db'
app.config['SECRET_KEY'] = '4b0c0a1a46a9468e69e54d9d'
CORS(app)
ma=Marshmallow(app)
db =SQLAlchemy(app)
from funii import routes