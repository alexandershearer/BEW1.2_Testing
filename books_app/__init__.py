from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from books_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

###########################
# Authentication
###########################

# TODO: Add authentication setup code here!

def setUp(self):
    """Executed prior to each test."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    self.app = app.test_client()
    db.drop_all()
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

bcrypt = Bcrypt(app)

###########################
# Blueprints
###########################

from books_app.main.routes import main as main_routes
app.register_blueprint(main_routes)

from books_app.auth.routes import auth as auth_routes
app.register_blueprint(auth_routes)

with app.app_context():
    db.create_all()