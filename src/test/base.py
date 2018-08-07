from src import app
import os
import unittest
import tempfile

from src.data.database import init_db, db_session
from src.data.models import User

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
