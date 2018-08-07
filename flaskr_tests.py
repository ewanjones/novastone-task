import flask
import os
import app
import unittest
import tempfile

class appTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    def test_can_login(self):
        with self.app:
            response = self.login('admin', 'password')
            assert response.status_code == 200
            assert response.get_json()['status'] == 'success'
            assert flask.session['logged_in'] == True 

    def test_invalid_username(self):
        with self.app:
            response = self.login('wrongusername', 'password')
            assert response.status_code == 403
            assert response.get_json()['status'] == 'failed'
            assert flask.session['logged_in'] == False

    def test_invalid_password(self):
        with self.app:
            response = self.login('admin', 'wrongpassword')
            assert response.status_code == 403
            assert response.get_json()['status'] == 'failed'
            assert flask.session['logged_in'] == False

    def test_logout(self):
        with self.app:
            self.login('admin', 'password')

            response = self.logout()
            assert response.status_code == 200 
            assert flask.session['logged_in'] == False


if __name__ == '__main__':
    unittest.main()
