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
from app import app_logger
from app.forms import AddNoteForm
from app.models import Note
from app.utils.note_utils import generate_title


logger = app_logger.new_logger(logger_name=__name__)


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
        logger.info(f'Title: {note_title}\nContent: {note_content}')
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

@bp.route(rule='/delete-note/id=<int:note_id>', methods=['GET'])
@login_required
def delete_note(note_id: int):
    note = Note.query.get(note_id)
    if note is None:
        flash(message='Invalid Note Id',
              category='error')
        return redirect(url_for('index.home'))
    if note.user_id != current_user.id:
        flash(message='Note not found',
              category='error')
        return redirect(url_for('index.home'))
    db.session.delete(note)
    try:
        db.session.commit()
        flash(message='Note Deleted.',
              category='info')
    except Exception as err:
        logger.error(f'Error Deleting Note - Note id: {note.id} - User id: {current_user.id}')
        logger.error(err)
        flash(message='Someting went wrond. Note could not be deleted.',
              category='error')
        db.session.rollback()
    return redirect(url_for('index.home'))
        
        
@bp.route(rule='/edit-note/id=<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id: int):
    note = Note.query.get(note_id)
    if note is None:
        flash(message='Invalid Note Id',
              category='error')
        return redirect(url_for('index.home'))
    
    edit_form = AddNoteForm()
    return render_template('notes/edit_note.html',
                           note=note,
                           add_form=edit_form,
                           edit_form=edit_form)