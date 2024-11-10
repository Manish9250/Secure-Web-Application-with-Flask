from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from backend.modals import User

class RegistrationForm(FlaskForm):
    def validate_username(self, username_to_check): # FlaskForm internally searches for validator funtions and impiments them
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists.")
        
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email already used.")

    username = StringField(label="", validators=[Length(min=3, max=30), DataRequired()])
    email = StringField(label="", validators=[Email(), DataRequired()])
    pwd1 = PasswordField(label="", validators=[Length(min=6), DataRequired()])
    pwd2 = PasswordField(label="", validators=[EqualTo("pwd1"), DataRequired()])
    submit = SubmitField(label="Submit")


class LoginForm(FlaskForm):
    username = StringField(label="", validators=[DataRequired()])
    password = PasswordField(label="", validators=[DataRequired()])
    submit = SubmitField(label="Login", validators=[DataRequired()])


class BuyForm(FlaskForm):
    submit = SubmitField(label="Buy")

class SellForm(FlaskForm):
    owned_item_name = HiddenField()
    submit = SubmitField(label="Sell")

class PaymentForm(FlaskForm):
    amount = StringField(label="")
    pin = StringField(label="")
    submit = SubmitField("Add Amount")
