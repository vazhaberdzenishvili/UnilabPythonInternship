from flask import Flask, render_template, flash, redirect, url_for
from flask_migrate import Migrate
import os
from flask_login import logout_user
from app.user.admin import admin
from flask_user import SQLAlchemyAdapter, UserManager,login_required
from app.database import db
from app.models import UserModel
from app.models.store import StoreModel
basedir = os.path.abspath(os.path.dirname(__file__))

migrate = Migrate()
# login_manager = LoginManager()
pages = (
    ("main.home_page", "Home"),
    ("main.about_us", "About"),
    ("UserModel.login", "Login"),
    ("UserModel.registration", "Register"),
    ("StoreModel.store", "Store")
)


def create_app():
    app = Flask(__name__)
    from app import models
    app.config['SECRET_KEY'] = "MYSecretKey236jkb56jk3b56bg54hg45y45h45"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CSRF_ENABLED'] = True
    app.config['USER_ENABLE_EMAIL'] = False
    db.init_app(app)
    migrate.init_app(app, db,render_as_batch=True)
    # login_manager.init_app(app)
    db_adapter = SQLAlchemyAdapter(db, UserModel)  # Setup the SQLAlchemy DB Adapter
    UserManager(db_adapter, app)  # Init Flask-User and bind to app
    from app.user.views import user_blueprint
    from app.store.views import store_blueprint
    from app.main.views import main_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(main_blueprint, url_prefix='/about')
    app.register_blueprint(user_blueprint, url_prefix="/UserModel")
    app.register_blueprint(store_blueprint, url_prefix="/StoreModel")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("მომხმარებელი გამოვიდა სისტემიდან")
        return redirect(url_for('main.home_page'))

    admin.init_app(app)
    return app

