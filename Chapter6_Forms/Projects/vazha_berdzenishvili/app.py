from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, email, equal_to

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JustASecretKey'


class RegistrationForm(FlaskForm):
    name = StringField("enter your Name", [DataRequired()])
    password = PasswordField("enter your password", [DataRequired(), length(min=8)])
    Repassword = PasswordField("Re-enter password", [equal_to("password", message="Passwords don't match")])
    email = StringField("enter your Email", [DataRequired(), email()])
    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired(), email()])
    password = PasswordField("Password", [DataRequired(), length(min=8)])
    submit = SubmitField("submit")


pages = (
    ("home", "Home"),
    ("login", "Login"),
    ("store", "Store"),
)
table_headers = ("ID", "Name", "Price", "Quantity")

table_rows = (
    ("1", "mouse", "15.00", 3),
    ("2", "keyboard", "30.00", 10),
    ("3", "headset", "64.99", 5),
    ("4", "webcam", "35", 2)
)

table = {
    "headers": table_headers,
    "rows": table_rows
}


@app.route('/')
def home():
    return render_template("home.html", pages=pages)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            session['name'] = form.name.data
            session['password'] = form.password.data
            session['Repassword'] = form.Repassword.data
            session['email'] = form.email.data
            flash(f"{session['name']},თქვენ წარმატებით გაიარეთ რეგისტრაცია")
            return redirect(url_for('login'))
        else:
            flash(f"თქვენ წარუმატებლად გაიარეთ რეგისტრაცია")
            return redirect(url_for('registration'))
    return render_template('register.html', form=form, pages=pages)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            session['email'] = form.email.data
            session['password'] = form.password.data
            flash(f"{session['email']},თქვენ წარმატებით გაიარეთ ავტორიზაცია")
            return redirect(url_for('store'))
        else:
            flash(f"თქვენ წარუმატებლად გაიარეთ რეგისტრაცია")
            return redirect(url_for('login'))
    return render_template('login.html', form=form, pages=pages)


@app.route('/store')
def store():
    return render_template('store.html', pages=pages, table=table)


if __name__ == "__main__":
    app.run(debug=True, port=8885)
