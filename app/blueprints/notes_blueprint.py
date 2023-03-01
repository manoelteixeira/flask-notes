# file: app/blueprints/notes_blueprints.py
from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask_login import login_required
from flask_login import current_user
from werkzeug.exceptions import abort
from app import db
from app import app_logger
from app.forms import AddNoteForm
from app.models import Note
from app.utils.note_utils import generate_title


logger = app_logger.new_logger(logger_name=__name__)


bp = Blueprint(name='notes', 
               import_name=__name__,
               url_prefix='/notes')

@bp.errorhandler(404)
def not_found(err):
    return render_template("4xx.html",
                           error=err)

@bp.errorhandler(403)
def forbiden(err):
    return render_template("4xx.html",
                    error=err)


@bp.route(rule='/add-note', methods=['GET', 'POST'])
@login_required
def add_note():
    add_form = AddNoteForm()
    if add_form.validate_on_submit():
        note_content = add_form.content.data
        note_title = add_form.title.data if add_form.title.data != '' else generate_title(note_content)
        new_note = Note(user_id=current_user.id,
                        title=note_title,
                        content=note_content)
        db.session.add(new_note)
        logger.info(f'Title: {note_title}\nContent: {note_content}')
        try:
            db.session.commit()
            flash(message='Note Created',
                    category='info')
            return redirect(url_for('index.home'))
            
        except Exception as err:
            flash(message='There was a problem saving your note.')
            logger.error('Note Not Added')
            logger.error(err)
            db.session.rollback()

    return render_template('notes/note.html',
                           title='Add Note',
                           form=add_form)


@bp.route(rule='/delete-note/id=<int:note_id>', methods=['GET'])
@login_required
def delete_note(note_id: int):
    ''' 
    delete_note()
    '''
    note = Note.query.get_or_404(ident=note_id,
                                 description='Note Not Found')
    if note.user_id != current_user.id:
        abort(403,
              description=f'{current_user.name} does not own this note.')
        
    db.session.delete(note)
    try:
        db.session.commit()
        flash(message='Note Deleted.',
              category='message')
    except Exception as err:
        logger.error(f'Error Deleting Note - Note id: {note.id} - User id: {current_user.id}')
        logger.error(err)
        flash(message='Someting went wrond. Note could not be deleted.',
              category='error')
        db.session.rollback()
    return redirect(url_for('index.home'))
        
@bp.route(rule='/edit-note/id=<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id: int):
    ''' 
    edit_note()
    '''
    note = Note.query.get_or_404(ident=note_id,
                                 description='Note Not Found')
    if note.user_id != current_user.id:
        abort(403,
              description=f'{current_user.name} does not own this note.')
    
    note_form = AddNoteForm(title=note.title,
                            content=note.content)
    if note_form.validate_on_submit():
        title = note_form.title.data
        content = note_form.content.data
        note.edit(title=title,
                  content=content)
        try:
            db.session.commit()
            flash(message='Note saved.',
                  category='message')
            return redirect(url_for('index.home'))
        except Exception as err:
            flash('Something whent wrong. Note could not be updated.',
                  category='error')
    return render_template('notes/note.html',
                           title='Edit Note',
                           form=note_form)