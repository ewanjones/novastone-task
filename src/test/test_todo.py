import flask
from src import app

from src.data.models import Todo
from .base import BaseTestCase

class TodoTestCase(BaseTestCase):
    def test_create_todo(self):
        data = { 'description': 'Finish test task' }
        self.app.post('/todo', data=data)

        todos = Todo.query.filter(description=data['description'])

        assert(len(todos), 1)

    
    def test_complete_todo(self):
        #  u = User('admin', 'password')
        #  db_session.add(u)
        #  db_session.commit()
        data = { 
            'description': 'Finish test task' ,
            'complete': 'true'
        }
        self.app.put('/todo', data=data)

        todos = Todo.query.filter(description=data['description'])

        assert(len(todos), 1)


