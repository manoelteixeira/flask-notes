# file: app/__init__.py
import sys
import os
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.exc import OperationalError
from app.utils import app_logger


db = SQLAlchemy()
login_manager = LoginManager()
logger = app_logger(logger_name=__name__,
                    output_filename='flask-note',
                    level='info')


def create_app(test_config: dict = None, config_file: str = None) -> Flask:
    """
    Create and setup flask instance
    TODO:
        - Exception handling on creating instance folder.
    """
    
    # Make sure instance folder exists
    logger.info('Making sure instance folder exists')
    if not os.path.isdir('instance'):
        os.makedirs('/instance')
        logger.info('creating instance folder')
    
    # Flask instance
    app = Flask(import_name=__name__,
                instance_relative_config=True)
    
    # Load Configuration
    logger.info('Loading configurations')
    if test_config:
        app.config.from_mapping(test_config)
    else:
        # Load configurations saved to the envionment
        app.config.from_prefixed_env(prefix='APP')
        if config_file:
            config_file_path = os.path.join(os.path.pardir, config_file)
            if not app.config.from_pyfile(filename=config_file_path, silent=True):
                logger.error('Failed to load configuration file.')
    
    # Check configuration
    config_list = ['SECRET_KEY',
                   'SQLALCHEMY_DATABASE_URI']
    for item in config_list:
        if not app.config.get(item):
            logger.warn(f'{item} not set')
            
    
    # Initializing Extentions            
    logger.info('Initializing Extentions')
    login_manager.init_app(app)
    db.init_app(app)
    
    # Add init-db command
    with app.app_context():
        app.cli.add_command(init_db)
        
    # Register blueprints (Routes)
    logger.info('Regitering blueprints')
    from app.blueprints import BLUEPRINTS
    
    for bp in BLUEPRINTS:
        logger.info(f'Route: {bp.name} added')
        app.register_blueprint(bp)
    
    @app.route(rule='/hello')
    def hello():
        return '<h1>Hello World</h1>'
    
    return app


# Flask App command line commands
@click.command('init-db')
def init_db():
    from app.models import Note
    from app.models import User
    try:
        logger.info('Creating database')
        db.drop_all()
        db.create_all()
    except OperationalError as err:
        logger.error('Trouble setting up database')
        logger.error(err)

