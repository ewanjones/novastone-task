from flask import Flask, jsonify
from .data.database import init_db, db_session
from .data.models import User

app = Flask(__name__)
init_db()

#  seed user
u = User('admin', 'password')
db_session.add(u)
db_session.commit()



@app.route('/signup')
def signup():
    return jsonify({'status': 'success'})

@app.route('/users')
def get_users():
    print(User.query.all())
    
    return jsonify({'status': 'success'})


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

