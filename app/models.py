from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import UserMixin

# Initialize Database Instance
db = SQLAlchemy()


# Helper table
words = db.Table('words',
                 db.Column('word_id', db.Integer, db.ForeignKey(
                     'word.id'), primary_key=True),
                 db.Column('user_id', db.Integer, db.ForeignKey(
                     'user.id'), primary_key=True)
                 )


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False, index=True)
    hash = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    words = db.relationship('Word', secondary=words, lazy='subquery',
                            backref=db.backref('user', lazy=True))

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


# Word model
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=True, nullable=False, index=True)
    entries = db.relationship('Entry', backref='word', lazy=True)


# Entry model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text, nullable=False, index=True)
    definition = db.Column(db.Text, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey(Word.id), nullable=False)
    examples = db.relationship('Example', backref='entry', lazy=True)


# Example model
class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey(Entry.id), nullable=False)


# Media uploaded by user model
class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    kind = db.Column(db.Text, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey(Word.id), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)


# Notes created by user model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey(Word.id), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
