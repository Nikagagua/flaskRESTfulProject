from datetime import datetime
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
import os

db_path = os.path.abspath('db.tasks')

app = Flask(__name__)

app.config['SECRET_KEY'] = 'RK7pY5GeN32tm9fHsk6rdM'
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255))
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'admin' and password == 'Str0ngPassw0rd':

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        access_token = create_access_token(identity=user.id)

        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# Get all tasks
@app.route('/tasks')
@jwt_required()
def get_tasks():
    tasks = db.session.query(Task).all()

    serialized_tasks = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        'priority': task.priority,
        'status': task.status
    } for task in tasks]
    return jsonify({'tasks': serialized_tasks}), 200


# Create a new task
@app.route('/create-task', methods=['POST'])
@jwt_required()
def create_task():
    title = request.json.get('title')
    description = request.json.get('description')
    due_date_str = request.json.get('due_date')
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

    priority = request.json.get('priority')
    status = request.json.get('status')

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    current_user = db.session.query(User).filter_by(id=User.id).first()

    if not current_user:
        return jsonify({'message': 'User not found'}), 404

    task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        status=status,
        user_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201


@app.route('/update-task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = db.session.query(Task).get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.get_json()

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    due_date_str = data.get('due_date', task.due_date)
    if due_date_str:
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)

    db.session.commit()

    return jsonify({'message': 'Task updated successfully'}), 200


@app.route('/delete-task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = db.session.query(Task).get(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
