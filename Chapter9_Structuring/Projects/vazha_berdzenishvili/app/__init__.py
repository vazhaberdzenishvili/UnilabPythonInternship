from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "MYSecretKey"

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app, db)

pages = (
    ("home", "Home"),
    ("UserModel.login", "Login"),
    ("UserModel.registration", "Register"),
    ("StoreModel.store", "Store")
)

from app.user.views import user_blueprint
from app.store.views import store_blueprint


app.register_blueprint(user_blueprint, url_prefix="/UserModel")
app.register_blueprint(store_blueprint, url_prefix="/StoreModel")


