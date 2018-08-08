import flask
from src import app

from src.data.database import db_session
from src.data.models import Todo, User
from .base import BaseTestCase

class TodoTestCase(BaseTestCase):
    def create_todo(self, description):
        data = { 'description': description }
        self.app.post('/todo', data=data)

    def test_create_todo(self):
        self.app.post('/login', data={            
            'username': 'test',
            'password': 'password'
        })
        self.create_todo('Finish task')

        todos = Todo.query.filter_by(description='Finish task', user_id=self.user.id)

        assert(todos.count(), 1)

    
    def test_complete_todo(self):
        data = { 
            'description': 'Finish test task' ,
            'complete': 'true'
        }
    
        #  cannot append todos here - todo.user_id NULL error
        user = User.query.filter_by(username='test').first()
        user.todos.append(Todo(data['description'], False, self.user.id))
        db_session.commit()
    
        self.app.put('/todo', data=data)
    
        todos = Todo.query.filter_by(description=data['description'])
    
        assert(todos.count(), 1)

