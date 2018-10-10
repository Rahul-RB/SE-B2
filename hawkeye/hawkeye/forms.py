from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
class SignupForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    submit = SubmitField("Sign In")
