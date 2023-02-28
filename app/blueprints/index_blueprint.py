# file: app/blueprints/index_blueprint.py
from datetime import datetime
import sqlalchemy.exc as sql_error
from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask_login import login_required
from flask_login import current_user
from app import app_logger
from app.models import Note
from app.forms import AddNoteForm

logger = app_logger.new_logger(logger_name=__name__)


bp = Blueprint(name='index', 
               import_name=__name__)


@bp.route(rule='/', methods=['GET', 'POST'])
def index():
    ''' 
    Home Page for logged out users
    '''
    if current_user.is_authenticated:
        flash(message=f'{current_user.username}',
              category='info')
        return redirect(url_for('index.home'))
            
    return render_template('notes/index.html')



@bp.route(rule='/home', methods=['GET'])
@login_required
def home():
    
    notes = Note.query.filter(Note.user_id==current_user.id).order_by(Note.last_modified.desc()).all()
    
    user_notes = enumerate(notes) if len(notes) > 0 else None
    
    return render_template('notes/home.html',
                           notes=user_notes)



@bp.route(rule='/profile', methods=['GET'])
@login_required
def profile():
    add_form = AddNoteForm()
    return render_template('notes/profile.html',
                           add_form=add_form)