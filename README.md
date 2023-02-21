# flask-notes
 
## Configuration file

- Example:
    ```python
    import os

    # Get the folder of the top-level directory of this project
    BASEDIR = os.path.abspath(os.path.dirname(__file__))


    # Update later by using a random number generator and moving
    # the actual key outside of the source code under version control
    SECRET_KEY = 'bad_secret_key'
    WTF_CSRF_ENABLED = True
    DEBUG = True

    # SQLAlchemy Configuration for sqlite 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```