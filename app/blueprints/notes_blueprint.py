# file: app/blueprints/notes_blueprints.py
from datetime import datetime
import sqlalchemy.exc as sql_error
from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask import Response
from flask_login import login_required
from flask_login import current_user
from app import db
from app.forms import AddNoteForm
from app.models import Note
from app.utils.note_utils import generate_title

from app.utils.app_logger import app_logger
logger = app_logger(logger_name=__name__,
                    output_filename='flask-note',
                    level='info')

bp = Blueprint(name='notes', 
               import_name=__name__,
               url_prefix='/notes')

@bp.route(rule='/add-note', methods=['POST'])
@login_required
def add_note():
    form = AddNoteForm()
    if form.validate_on_submit():
        note_content = form.content.data
        note_title = form.title.data if form.title.data != '' else generate_title(note_content)
        new_note = Note(user_id=current_user.id,
                        title=note_title,
                        content=note_content)
        db.session.add(new_note)
        try:
            db.session.commit()
            flash(message='Note Created',
                  category='info')
        except Exception as err:
            flash(message='There was a problem saving your note.')
            logger.error('Note Not Added')
            logger.error(err)
            db.session.rollback()
            
        
    req_ref = request.referrer
    if req_ref is not None and 'profile' in req_ref:
        return redirect(url_for('index.profile'))
    elif req_ref is not None and 'home' in req_ref:
        return redirect(url_for('index.home'))
    else:
        return Response(status="200 OK")
