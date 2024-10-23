from application import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    about_user = db.Column(db.String(200))
    users_data = db.relationship('UserData', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set password hash for the user."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user instance to a dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'about_user': self.about_user
        }
    
class UserData(db.Model):
    __tablename__ = 'user_data' 

    id = db.Column(db.Integer, primary_key=True)
    about = db.Column(db.String(500)) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  

    def __repr__(self):
        return f'<UserData {self.id} for User {self.user_id}>'
