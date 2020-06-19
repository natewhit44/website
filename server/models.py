from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from server import db, login_manager
from flask_login import UserMixin
from flask import current_app

# Decorator to load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# DB models/table definitions
class User(db.Model, UserMixin):
    # Column definitions
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # Relationship to post table
    posts = db.relationship('Post', backref='author', lazy=True)

    # Password functions
    def get_reset_token(self, expires_sec=1800):
        # Initialize serializer
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)

        # Create token
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        # Initialize serializer
        s = Serializer(current_app.config['SECRET_KEY'])

        # Try to load token
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # String representation of class member
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    # Column definitions
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # Foreign key defintion
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # String representation of class member
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
