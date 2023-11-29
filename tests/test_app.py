import pytest
from app import app, db, Task


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200


def test_create_task(client):
    data = {'title': 'Test Task', 'description': 'This is a test task.'}
    response = client.post('/create-task', json=data)
    assert response.status_code == 201


def test_update_task(client):
    task_data = {'title': 'Initial Task Title', 'description': 'Initial task description'}
    create_response = client.post('/create-task', json=task_data)
    assert create_response.status_code == 201

    # Update the task
    update_data = {'title': 'Updated Task Title'}
    response = client.put('/update-task/1', json=update_data)
    assert response.status_code == 200

    updated_task = db.session.query(Task).get(1)
    assert updated_task.title == 'Updated Task Title'


def test_delete_task(client):
    task_data = {'title': 'Task to Delete', 'description': 'Task to delete description'}
    create_response = client.post('/create-task', json=task_data)
    assert create_response.status_code == 201

    response = client.delete('/delete-task/1')
    assert response.status_code == 200

    deleted_task = db.session.query(Task).get(1)
    assert deleted_task is None
