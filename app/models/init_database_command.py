# file : app/models/init_database_command.py
import click
from sqlalchemy.exc import OperationalError
from app import db
from app import app_logger
from .note_model import Note
from .user_model import User


logger = app_logger.new_logger(logger_name=__name__)


# Flask App command line commands
@click.command('init-db')
def init_db():
    logger.info("Initializing Database")
    try:
        db.drop_all()
        db.create_all()
        logger.info("Database created.")
    except OperationalError as err:
        logger.error('Trouble setting up database')
        logger.error(err)
        
        
        

