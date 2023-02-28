# file: app/__init__.py
import os
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.utils import AppLogger

db = SQLAlchemy()
login_manager = LoginManager()
app_logger = AppLogger(level='info')



def create_app(test_config: dict = None, config_file: str = None) -> Flask:
    """
    Create and setup flask instance
    TODO:
        - Exception handling on creating instance folder.
    """
    
    # Flask instance
    app = Flask(import_name=__name__,
                instance_relative_config=True)
    
    # Make sure instance folder exists
    if not os.path.isdir('instance'):
        os.makedirs('instance')
        
    if test_config:
        app.config.from_mapping(test_config)
    else:
        # Load Configuration
        if config_file:
            config_file_path = os.path.join(os.path.pardir, config_file)
            app.config.from_pyfile(filename=config_file_path, silent=True)
        
        # Prefixed environment variable will replace those set on config file
        app.config.from_prefixed_env(prefix='APP')
    
    # Check configuration
    config_list = ['SECRET_KEY',
                   'SQLALCHEMY_DATABASE_URI']
    
    for item in config_list:
        if not app.config.get(item):
            raise Exception(f'{item} not Set')
            
    # Initializing Extentions            
    login_manager.init_app(app)
    db.init_app(app)
    app_logger.init_app(app)
       
    # Add init-db command
    from app.models import init_db
    with app.app_context():
        app.cli.add_command(init_db)
        
    # Register blueprints (Routes)
    from app.blueprints import BLUEPRINTS
    
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
    
    
    return app
