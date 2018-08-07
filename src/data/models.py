from src import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin

from .database import Base

db = SQLAlchemy(app)


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50), unique=False)
    todos = db.relationship('Todo', backref='users', lazy=True)

    def __init__(self, username=None, password=None):
        self.username = username 
        self.password = password 

    def __repr__(self):
        return '<User %r>' % (self.username)


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, unique=False)
    complete = Boolean()

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        nullable=False
    )

    def __init__(self, description=None, complete=False, user_id=None):
        self.description = description 
        self.complete = complete
        self.user_id = user_id 

    def __repr__(self):
        return '<Todo %r>' % (self.description)
