# file: app/forms/note_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired

class AddNoteForm(FlaskForm):
    title = StringField(label='Title')
    content = TextAreaField(label='New Note',
                            validators=[DataRequired(message='You need to type someting.')])
    submit = SubmitField(label='Add Note')