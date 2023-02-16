# file: app/models/user_model.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # Table columns:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True, nullable=False)
    email = db.Column(db.String, index=True, unique=True, nullable=False)
    name = db.Column(db.String, index=True, unique=False, nullable=False)
    joined_at = db.Column(db.DateTime(), index=True, unique=False, nullable=False)
    password = db.Column(db.String)
    # Relationship:
    # One User has many notes (1 -> *)
    notes = db.relationship('Note', backref='user', lazy='dynamic', cascade='all, delete, delete-orphan')
    
    # Class Methods
    def __init__(self, name:str, username:str, email:str, password:str) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.set_password(password=password)
        self.joined_at = datetime.utcnow()
        
    
    def __repr__(self) -> str:
        return f"<id: {self.id} - username: {self.username} - joined at: {self.joined_at.date()}>"
    
    
    def set_password(self, password:str) -> None:
        '''
        Generate and store the hash from the given password.
        password: String, password
        '''
        self.password = generate_password_hash(password=password)
        
        
    def check_password(self, password:str) -> bool:
        '''
        Check if the hash of given password is equal to the stored hash.
        password: String, password
        '''
        return check_password_hash(pwhash=self.password, password=password)