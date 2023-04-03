# file: app/blueprints/auth_blueprints.py
from sqlalchemy.exc import IntegrityError
from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from app import db
from app import login_manager
from app import app_logger
from app.forms import RegisterForm
from app.forms import LoginForm
from app.models import User


logger = app_logger.new_logger(logger_name=__name__)

bp = Blueprint(name='auth',
               import_name=__name__,
               url_prefix='/auth')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in.",
          category='error')
    return redirect(url_for('auth.login'))



@bp.route(rule='/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        logger.info(current_user)
        flash('User already logged in.',
              category='info')
        return redirect(url_for('index.home'))
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            flash(message='Username not found.',
                  category='error')
        elif not user.check_password(password=login_form.password.data):
            flash(message='Password is incorrect',
                  category='error')
        else:
            login_user(user= user, remember=login_form.remember.data)
            return redirect(url_for('index.home'))
    
    return render_template('auth/login.html',
                           form=login_form)



@bp.route(rule='/logout', methods=['GET'])
@login_required
def logout():
    flash(message=f'{current_user.username} Logged off.',
          category='info')
    logout_user()
    return redirect(url_for('auth.login'))



@bp.route(rule='/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(name=form.name.data,
                            username=form.username.data,
                            email=form.email.data,
                            password=form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))
            except IntegrityError as err:
                logger.info(f'Faild to register {new_user}')
                args = err.args
                if any('username' in arg for arg in args):
                    flash('Username already taken.',
                        category='error')
                elif any('email' in arg for arg in args):
                    flash('Email already in use.',
                        category='error')
                db.session.rollback()
        
    return render_template('auth/register.html',
                           form=form)

