from app import db


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


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, firstname, lastname, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email

    def __repr__(self):
        return f" Name: {self.firstname} {self.lastname}, Password: {self.password}, Email: {self.email} "

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
