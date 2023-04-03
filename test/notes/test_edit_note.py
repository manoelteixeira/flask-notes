# file: test/notes/test_edit_note.py
'''
Test Edit Route
'''
from app.models import Note
from app.models import User
from datetime import datetime


def test_edit_note_without_login(test_client, test_note):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/edit-note' page is posted without a valid user logged 
    THEN check if response is displayed correctly
    '''
    note = Note.query.get(test_note.id)
    
    response = test_client.get(f'/notes/edit-note/id={note.id}',
                               follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Please log in.' in response_data
    assert 'Notes' in response_data
    assert 'Login' in response_data

def test_edit_other_user_note(test_client, test_logged_user, test_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/edit-note' page is posted valid user logged and invalid values
    THEN check if new note was stored and displayed correctly
    '''
    # assert False
    note = Note.query.filter(Note.user_id != test_user.id).first()
    
    response = test_client.get(f"/notes/edit-note/id={note.id}",
                               follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Error 403: Forbidden' in response_data
    assert f'Oops! {test_user.name} does not own this note.'
    
    edited_note = Note.query.get(note.id)
    
    assert edited_note
    
    
def test_edit_note(test_client, test_logged_user, test_user):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/edit-note' page is posted valid user logged and valid values
    THEN check if new note was stored and displayed correctly
    '''
    
    note = Note.query.filter(Note.user_id == test_user.id).first()
    title = note.title
    content = note.content
    created_at = note.created_at
    last_modified = note.last_modified
    
    response = test_client.post(f"/notes/edit-note/id={note.id}",
                               data=dict(title='Edited Note',
                                         content=f'{note.content}\nEdited Note'),
                               follow_redirects=True)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert 'Note saved' in response_data
    
    edited_note = Note.query.get(note.id) 
    assert title != edited_note.title
    assert content != edited_note.content
    assert created_at == edited_note.created_at
    assert last_modified < edited_note.last_modified
    
    
    

