from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db

login_manager = LoginManager()
login_manager.login_view = 'UserModel.login'


# login_manager.login_message = 'info'


class StoreModel(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f" Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def add_item(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    email = db.Column(db.String, unique=True, nullable=False, index=True)
    active = db.Column(db.Boolean(), nullable=False, server_default='1')

    def __init__(self, firstname, lastname, username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def __repr__(self):
        return f" Name: {self.firstname} {self.lastname}, Password: {self.password}, Email: {self.email} "

    roles = db.relationship('Role', secondary='user_roles', )

    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id,
        self.role_id = role_id

    def __repr__(self):
        return f"user_id[{self.user_id}] to role_id[{self.user_role}]"


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)
