'''
Test Delete Route
'''
from app.models import Note
from app.models import User
from datetime import datetime


def test_delete_note_without_login(test_client, test_note):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/delete-note' page is posted without a valid user logged 
    THEN check if response is displayed correctly
    '''
    note = Note.query.get(test_note.id)
    response = test_client.get(f'/notes/delete-note/id={note.id}',
                               follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Please log in.' in response_data
    assert 'Notes' in response_data
    assert 'Login' in response_data

def test_delete_other_user_note(test_client, test_logged_user, test_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/delete-note' page is posted valid user logged and invalid values
    THEN check if new note was stored and displayed correctly
    '''
    note = Note.query.filter(Note.user_id != test_user.id).first()
    response = test_client.get(f"/notes/delete-note/id={note.id}",
                               follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Note not found' in response_data
    deleted_note = Note.query.get(note.id)
    assert deleted_note
    
    
def test_delete_note(test_client, test_logged_user, test_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/delete-note' page is posted valid user logged and valid values
    THEN check if new note was stored and displayed correctly
    '''
    note = Note.query.filter(Note.user_id == test_user.id).first()
    response = test_client.get(f"/notes/delete-note/id={note.id}",
                               follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Note Delete' in response_data
    deleted_note = Note.query.get(note.id)
    assert deleted_note is None
    
    

