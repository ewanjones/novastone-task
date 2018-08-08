from flask import request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user

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
        todos = current_user.todos 
        items = [{
            'description': td.description,
            'complete': td.complete
        } for td in todos]
        
        return jsonify({
            'status': 'success',
            'todos': items
        })

    
    if request.method == "POST":
        description = request.form.get('description', None)

        if not description:
            return jsonify({
                'status': 'failed',
                'reason': 'description required'
            }), 404

        todo = Todo(description=description)
        current_user.todos.append(todo)
        db_session.commit()

        return jsonify({
            'status': 'sucess',
            'todo': {
                'id': todo.id,
                'description': todo.description,
                'complete': todo.complete
            }
        })


    if request.method == "PUT":
        body = request.get_json()
        todo_id = body.get('id') 
        complete = body.get('complete') 

        if not todo_id:
            return jsonify({
                'status': 'failed',
                'reason': 'todo not found'
            }), 404

        todo = Todo.query.get(todo_id)
        todo.complete = True if complete == 'true' else False
        db_session.commit()

        return jsonify({ 'status': 'sucess' })


    if request.method == "DELETE":
        body = request.get_json()
        todo_id = body.get('id') 

        if not todo_id:
            return jsonify({
                'status': 'failed',
                'reason': 'todo not found'
            }), 404

        todo = Todo.query.get(todo_id)
        db_session.delete(todo)
        db_session.commit()

        return jsonify({ 'status': 'sucess' })
