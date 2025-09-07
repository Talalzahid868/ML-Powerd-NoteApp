from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from noteapp import db,login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(150),nullable=False)
    notes=db.relationship('Note',backref='author',lazy=True)
    def __repr__(self):
        return f"User('{self.id},{self.username},{self.email},{self.password},{self.notes}')"
    

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(100))   # Auto-tagging result
    keywords = db.Column(db.String(300))   # Extracted keywords
    summary = db.Column(db.Text)           # Auto-generated summary
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   
    def __repr__(self):
        return f"Note('{self.id},{self.title},{self.content})"
    
     


