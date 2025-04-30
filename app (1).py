from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='tasks')

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Task Management APIs

# GET: Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_json = [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'assigned_to': task.assigned_to
        }
        for task in tasks
    ]
    return jsonify(tasks_json), 200

# GET: Retrieve a task by ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task:
        task_json = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'assigned_to': task.assigned_to
        }
        return jsonify(task_json), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

# POST: Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    if 'title' not in data or 'status' not in data or 'assigned_to' not in data:
        return jsonify({'error': 'Title, status, and assigned_to are required'}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data['status'],
        assigned_to=data['assigned_to']
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status}), 201

# PUT: Update an existing task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.assigned_to = data.get('assigned_to', task.assigned_to)

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200

# DELETE: Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

# User Management APIs

# POST: Register a new user
@app.route('/users', methods=['POST'])
def register_user():
    data = request.json
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']  # Note: You should hash passwords in production!
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201

# GET: Retrieve a user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        user_json = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return jsonify(user_json), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# PUT: Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)  # Note: Hash passwords in production

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# DELETE: Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True) 
