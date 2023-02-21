# file: test/models/test_user_model.py
'''
Test Note Model
'''
import pytest
import warnings
from datetime import datetime
from app.models import Note


def test_new_note(test_user):
    '''
    GIVEN a new Note model
    WHEN a new Note is created
    THEN check the user_id, title, content and created_at 
         are defined correctly.
    '''
    
    title='Test Note Title'
    content='Test Note Content'
    
    new_note = Note(
        user_id=test_user.id,
        title=title,
        content=content
    )
    new_note.id = 1
    
    assert new_note.user_id == test_user.id
    assert new_note.title == title
    assert new_note.content == content
    assert new_note.created_at <= datetime.utcnow()
    assert new_note.created_at == new_note.last_modified
    
    repr_str = f"< id: { new_note.id} - user_id: { new_note.user_id} - created at: { new_note.created_at}>"
    assert new_note.__repr__() == repr_str
    
def test_note_edit_title_and_content(test_note):
    '''
    GIVEN a Note model
    WHEN the method edit is called with all parametes (title and content) set
    THEN check if title, content and last_modified are updated correctly.
    '''
    old_title = test_note.title
    old_content = test_note.content
    
    assert test_note.created_at == test_note.last_modified
    
    new_title='Test Note Edited Title'
    new_content='Test Note Edited Content'
    
    test_note.edit(title=new_title,
                       content=new_content)
    
    assert test_note.title != old_title
    assert test_note.content != old_content
    assert test_note.title == new_title
    assert test_note.content == new_content
    assert test_note.last_modified <= datetime.utcnow()
    assert test_note.created_at < test_note.last_modified
    
def test_note_edit_only_title(test_note):
    '''
    GIVEN a Note model
    WHEN the method edit is called with only a new title given.
    THEN check if title and last_modified are updated correctly.
    '''
    old_title = test_note.title
    old_content = test_note.content
    
    new_title='Test Note only Title Edited'
    
    
    test_note.edit(title=new_title)
    
    assert test_note.title != old_title
    assert test_note.title == new_title
    assert test_note.content == old_content
    assert test_note.last_modified <= datetime.utcnow()
    assert test_note.created_at < test_note.last_modified
    
def test_note_edit_only_content(test_note):
    '''
    GIVEN a Note model
    WHEN the method edit is called with only a new content given.
    THEN check if title and last_modified are updated correctly.
    '''
    old_title = test_note.title
    old_content = test_note.content
    
    new_content='Test Note Only Content Edited'
    
    test_note.edit(content=new_content)
    
    assert test_note.title == old_title
    assert test_note.content != old_content
    assert test_note.content == new_content
    assert test_note.last_modified <= datetime.utcnow()
    assert test_note.created_at < test_note.last_modified
    
def test_note_edit_no_changes(test_note):
    '''
    GIVEN a Note model
    WHEN the method edit is called but nothing is changed.
    THEN check if raizes exception
    '''
    
    with pytest.warns(UserWarning, match='Nothing was changed.'):
        test_note.edit()
