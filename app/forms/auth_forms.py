# file: app/forms/auth_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length

class RegisterForm(FlaskForm):
    name = StringField(label='Name',
                       validators=[DataRequired()],
                       description='First and last name')
    username = StringField(label='Username',
                           validators=[DataRequired(),
                                       Length(min=4,
                                              message=f'Username must be at least {min} long')])
    email = EmailField(label='Email',
                       validators=[Email()])
    password = PasswordField(label='Password',
                             validators=[DataRequired(),
                                         Length(min=6,
                                                message='Password must have at least 6 characters')
                                         ],
                             description='At Least 6 characters.')
    confirm = PasswordField(label='Re-enter password',
                            validators=[DataRequired(),
                                        EqualTo(fieldname='password',
                                                message='Password must match'),
                                        ])
    submit = SubmitField(label='Register')
    

class LoginForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired()])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    remember = BooleanField(label='Remember me.')
    submit = SubmitField(label='Login')
    
