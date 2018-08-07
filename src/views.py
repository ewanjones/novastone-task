from flask import request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required

from . import app
from src.data.models import User, Todo

@app.route('/')
def hello():
    return 'hello world'

@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        session['logged_in'] = False
        return jsonify({
            'status': 'failed',
            'reason': 'invalid username or password'
        }), 403

    session['logged_in'] = True
    login_user(user)

    return jsonify({'status': 'success'})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return jsonify({'status': 'success'})


@app.route('/todo', methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def todo():
    if request.method == "GET":
        print(current_user.todos) 
    
    if request.method == "POST":
        description = request.form.get('description', None)

        if not description:
            return jsonify({
                'status': 'failed',
                'reason': 'description required'
            })

        todo = Todo(description=description)
        current_user.todos.append(todo)
