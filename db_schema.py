from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(20), unique=True)
    fname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(254), unique=True)
    password_hash = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.now())
    # verified = db.Column(db.Boolean, default=False)

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash
