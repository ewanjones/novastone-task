from src import app
import os
import unittest
import tempfile

from src.data.database import init_db, db_session
from src.data.models import User, Todo

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            init_db()

        self.user = User('test', 'password')
        db_session.add(self.user)
        db_session.commit()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        db_session.delete(self.user)
        db_session.commit()
