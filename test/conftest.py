# file: test/conftest.py
import pytest
from os import unlink
from os import path

from app import create_app, db
from app.models import User
from app.models import Note
from app.utils import app_logger

logger = app_logger(logger_name=__name__,
                    output_filename='test-flask-note',
                    level='info')


@pytest.fixture(scope='module')
def test_user():
    '''
    Default User Instance
    '''
    new_user = User(
        username='testTuser01',
        name='First Test User',
        email='first_user@test.com',
        password='badTestPassword'
    )
    new_user.id = 1
    return new_user


@pytest.fixture(scope='module')
def test_note(test_user):
    '''
    Default Note Instance
    '''
    new_note = Note(user_id=test_user.id,
                    title='Test Note Title',
                    content='Test Note Content'
                    )
    new_note.id = 1
    
    return new_note


@pytest.fixture(scope='module')
def test_app():
    
    config = {'SECRET_KEY':'bad_secret_key',
              'WTF_CSRF_ENABLED':True,
              'SQLALCHEMY_DATABASE_URI':'sqlite:///test_app_data.sqlite',
              'SQLALCHEMY_TRACK_MODIFICATIONS':False,
              'DATABASE_PATH':'instance/test_app_data.sqlite',
              'TESTING':True,
              'WTF_CSRF_ENABLED':False}
    
    app = create_app(test_config=config)
    if path.isfile(app.config['DATABASE_PATH']):
        unlink(app.config['DATABASE_PATH'])
    
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            db.drop_all()
            db.create_all()
    yield app  
    unlink(app.config['DATABASE_PATH'])
    
@pytest.fixture(scope='module')
def test_db(test_app, test_user, test_note):
    new_user = User(
        username='testTuser02',
        name='Second Test User',
        email='second_user@test.com',
        password='badTestPassword2'
    )
    new_user.id = 2
    
    new_note = Note(user_id=new_user.id,
                    title='Test Note Title',
                    content='Test Note Content'
                    )
    
    with test_app.app_context():
        db.session.add(test_user)
        db.session.add(new_user)
        db.session.add(test_note)
        db.session.add(new_note)
        db.session.commit()
        
        yield db 
        
@pytest.fixture(scope='module')
def test_client(test_app, test_db):
    with test_app.test_client() as test_client:
        yield test_client
        
@pytest.fixture(scope='module')
def test_logged_user(test_client, test_user):
    test_client.post('auth/login',
                     data=dict(username=test_user.username,
                               password='badTestPassword'),
                     follow_redirects=True)
    yield # this is where the testing happens!
    
    test_client.get('/logout',
                    follow_redirects=True)