import flask
from src import app
import os
from src.data.models import User
from .base import BaseTestCase

class AuthTestCase(BaseTestCase):
    def login(self, username, password):
        return self.app.post('/login', data={            
            'username': username,
            'password': password
        })

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def test_can_login(self):
        with app.app_context():
            with self.app:
                response = self.login('test', 'password')
                assert response.status_code == 200
                assert response.get_json()['status'] == 'success'
                assert flask.session['logged_in'] == True 

    def test_invalid_username(self):
        with app.app_context():
            with self.app:
                response = self.login('wrongusername', 'password')
                assert response.status_code == 403
                assert response.get_json()['status'] == 'failed'
                assert flask.session['logged_in'] == False

    def test_invalid_password(self):
        with app.app_context():
            with self.app:
                response = self.login('test', 'wrongpassword')
                assert response.status_code == 403
                assert response.get_json()['status'] == 'failed'
                assert flask.session['logged_in'] == False

    def test_logout(self):
        with app.app_context():
            with self.app:
                self.login('test', 'password')

                response = self.logout()
                assert response.status_code == 200 
                assert flask.session['logged_in'] == False

