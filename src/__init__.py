from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required

from .data.database import DB_PATH, init_db, db_session

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = DB_PATH
app.config.from_object(__name__)
app.secret_key = '\xeao\x87f\xc4\xd5\x0f\xaaG\xa6\xb8~\xcd\xbd\xf3%;\x1d\xab\xebv\xa2\xbc'

import src.views
init_db()

#  session config
SESSION_TYPE = 'sqlalchemy'
SESSION_SQLALCHEMY_TABLE = 'sessions'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = DB_PATH

app.config.from_object(__name__)
session_obj = Session(app)
session_obj.app.session_interface.db.create_all()

#  login config
login_manager = LoginManager()
login_manager.init_app(app)
from .auth import load_user

#  seed user
#  u = User('admin', 'password')
#  db_session.add(u)
#  db_session.commit()





@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

