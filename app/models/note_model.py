# file: app/models/note_model.py
import markdown
from warnings import warn
from datetime import datetime
from app import db


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), index=True, unique=False, nullable=False)
    content = db.Column(db.String(), index=True, unique=False, nullable=False)
    created_at = db.Column(db.DateTime(), index=True, unique=False, nullable=False)
    last_modified = db.Column(db.DateTime(), index=True, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Foreign Key
    
    def __init__(self, user_id:int, title:str, content:str) -> None:
        self.user_id = user_id
        self.title = title
        # self.content = content.replace('\n','<br>')
        self.content = content
        self.created_at = self.last_modified = datetime.utcnow()
        
        
    def __repr__(self) -> str:
        return f"< id: {self.id} - user_id: {self.user_id} - created at: {self.created_at}>"
    
    @property
    def content_md(self) -> str:
        return markdown.markdown(self.content.replace('\n','<br>'))
    
    def edit(self, title:str=None, content:str=None) -> None:
        title_changed = False
        content_canged = False
        if title or content:
            if title is not None and title != self.title:
                self.title = title
                title_changed = True
            if content is not None and content != self.content:
                self.content = content
                content_canged = True
        if title_changed or content_canged:
            self.last_modified = datetime.utcnow()
        else:
            warn('Nothing was changed.')