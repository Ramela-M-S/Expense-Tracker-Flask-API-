from flask import Flask
from flask_login import LoginManager


app= Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"

from flask_sqlalchemy import SQLAlchemy
app.config['SECRET_KEY'] = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

from eta import route
from eta import resource