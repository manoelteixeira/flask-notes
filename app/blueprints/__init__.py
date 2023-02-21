# file: app/blueprints/__init__.py
from app.blueprints.index_blueprint import bp as index_bp
from app.blueprints.auth_blueprint import bp as auth_bp
from app.blueprints.notes_blueprint import bp as notes_bp

BLUEPRINTS = [index_bp,
              auth_bp,
              notes_bp]