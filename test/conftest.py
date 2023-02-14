import pytest

from app.models import User
from app.models import Note


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