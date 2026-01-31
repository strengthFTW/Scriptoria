from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship
    stories = db.relationship('Story', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

class Story(db.Model):
    """Story model for saving generated screenplays"""
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(50))
    story_idea = db.Column(db.Text)
    screenplay = db.Column(db.Text, nullable=False)
    characters = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Story {self.title}>'
    
    def to_dict(self, include_content=True):
        """Convert story to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'genre': self.genre,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        
        if include_content:
            data.update({
                'story_idea': self.story_idea,
                'screenplay': self.screenplay,
                'characters': self.characters
            })
        
        return data

