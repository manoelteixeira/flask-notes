# file: app/forms/login_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired()])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    remember = BooleanField(label='Remember me.')
    submit = SubmitField(label='Login')