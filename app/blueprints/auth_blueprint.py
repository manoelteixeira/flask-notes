import sqlalchemy.exc as sql_error
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
from app.forms import RegisterForm
from app.forms import LoginForm
from app.models import User


bp = Blueprint(name='auth',
               import_name=__name__,
               url_prefix='/auth')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in.")
    return redirect(url_for('auth.login'))

@bp.route(rule='/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash('User already logged in.')
        return redirect(url_for('index.home'))
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            flash(message='Username not found.',
                  category='info')
        elif not user.check_password(password=login_form.password.data):
            flash(message='Password is incorrect',
                  category='info')
        else:
            login_user(user= user, remember=login_form.remember.data)
            return redirect(url_for('index.home'))
    
    return render_template('auth/login.html',
                           form=login_form)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(message='User Logged off.',
          category='info')
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
            except sql_error.IntegrityError as err:
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

