from sqlalchemy import Column, Integer, String
from .database import Base
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50), unique=False)

    def __init__(self, username=None, password=None):
        self.username = username 
        self.password = password 

    def __repr__(self):
        return '<User %r>' % (self.username)
