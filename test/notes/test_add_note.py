# file: test/notes/test_add_note.py
'''
Test Notes Route
'''
from app.models import Note
from app.models import User
from datetime import datetime


def test_add_new_note_without_login(test_client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/notes/add-note' page is posted without a valid user logged 
    THEN check if new note was stored and displayed correctly
    '''
    
    note_title='Test Note'
    note_content='This is a test note.'
    response = test_client.post('/notes/add-note',
                                data=dict(title=note_title,
                                    content=note_content),
                                follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Please log in.' in response_data
    assert 'Register' in response_data
    assert 'Notes' in response_data
    assert 'Login' in response_data


def test_add_new_note(test_logged_user, test_client, test_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/notes/add-note' page is posted with a valid user logged and valid values
    THEN check if new note was stored and displayed correctly
    '''
    
    note_title = 'Test Note Title'
    note_content = 'Test Note Content'
    response = test_client.post('/notes/add-note',
                                data=dict(title=note_title,
                                    content=note_content),
                                follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    # Check if note was saved correctly
    note = Note.query.filter_by(title=note_title).first()
    user = User.query.filter_by(username=test_user.username).first()
    
    assert note.title == note_title
    assert note.content == note_content
    assert note.created_at <= datetime.utcnow()
    assert note.user_id == user.id
    
    

