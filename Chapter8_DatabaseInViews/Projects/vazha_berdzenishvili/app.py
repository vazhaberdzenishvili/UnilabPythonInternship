from flask import Flask, redirect, request, url_for, flash, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm, StoreForm
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "MYSecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

pages = (
    ("home", "Home"),
    ("login", "Login"),
    ("store", "Store"),
)
table_headers = ("ID", "Name", "Price", "Quantity")


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


@app.route('/')
def home():
    return render_template("home.html", pages=pages)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            password = form.password.data
            email = form.email.data
            user = UserModel(firstname, lastname, password, email)
            if UserModel.find_by_email(email) is None:
                user.add_user()
                flash(f"{firstname},თქვენ წარმატებით გაიარეთ რეგისტრაცია")
                return redirect(url_for('login'))
            else:
                flash(f"მომხმარებელი {email} ელფოსტით უკვე დარეგისტრირებულია")
            return redirect(url_for('registration'))
    return render_template('register.html', form=form, pages=pages)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user:
                if user.password == password:
                    flash(f"{email},თქვენ წარმატებით გაიარეთ ავტორიზაცია")
                    return redirect(url_for('store'))
                else:
                    flash(f"პაროლი არასწორია")
                    return redirect(url_for('login'))
            flash(f"{email} ელფოსტით მომხმარებელი არ არის რეგისტრირებული")
    return render_template('login.html', form=form, pages=pages)


@app.route('/store', methods=['GET', 'POST'])
def store():
    data = StoreModel.query.all()
    return render_template('store.html', pages=pages, items=data)


@app.route('/add', methods=['GET', 'POST'])
def Store_add():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    item = StoreModel(name, price, quantity)
    if StoreModel.find_by_name(name) is None:
        item.add_item()
        flash(f" ნივთი {name} წარმატებით დაემატა ბაზაში")
        return redirect(url_for('store'))
    else:
        flash(F"პროდუქტი {name} დასახელებით უკვე არსებობს ")
        return redirect(url_for('store'))

    # form = StoreForm()
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         name = form.name.data
    #         price = form.price.data
    #         quantity = form.quantity.data
    #         item = StoreModel(name, price, quantity)
    #         if StoreModel.find_by_name(name) is None:
    #             item.add_item()
    #             flash(f" ნივთი {name} წარმატებით დაემატა ბაზაში")
    #             return redirect(url_for('Store'))
    #         else:
    #             flash("დამატებისას წარმოიშვა პრობლემა ")
    #         return redirect(url_for('Store'))
    #     return render_template('add_item_store.html', pages=pages, form=form)


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def store_delete(id):
    item = StoreModel.query.get(id)
    if item == 1:
        flash("მინიმუმ 1 პროდუქცი უნდა იყოს ბაზაში")
    else:
        item.delete_item()
        flash("პროდუქტი  წარმატებით წაიშალა ბაზიდან")

    return redirect(url_for('store'))


@app.route('/update', methods=['GET', 'POST'])
def store_edit():
    if request.method == 'PObST':
        item_data = StoreModel.query.get(request.form.get('id'))
        item_data.name = request.form['name']
        item_data.price = request.form['price']
        item_data.quantity = request.form['quantity']
        db.session.commit()
        flash(f"პროდუქტი  {item_data.name}  წარმატებით განახლდა ")
        return redirect(url_for('store'))


if __name__ == "__main__":
    app.run(debug=True, port=8885)
