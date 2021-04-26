from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, email, equal_to


class RegistrationForm(FlaskForm):
    firstname = StringField("enter your Name", [DataRequired()])
    lastname = StringField("enter your Name", [DataRequired()])
    password = PasswordField("enter your password", [DataRequired(), length(min=8)])
    Repassword = PasswordField("Re-enter password", [equal_to("password", message="Passwords don't match")])
    email = StringField("enter your Email", [DataRequired(), email()])
    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired(), email()])
    password = PasswordField("Password", [DataRequired(), length(min=8)])
    submit = SubmitField("submit")


class StoreForm(FlaskForm):
    name = StringField("Product Name", [DataRequired()])
    price = StringField("Price", [DataRequired()])
    quantity = StringField("Quantity", [DataRequired()])
    submit = SubmitField("Add")
