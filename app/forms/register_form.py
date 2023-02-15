# file: app/forms/register_form.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length

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
    

              
              
 