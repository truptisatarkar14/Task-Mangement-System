import unittest
import json
from app import app
from models import Task, User, connect_db

class TaskManagementTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

        # Initialize the database and tables
        self.init_database()

    def tearDown(self):
        # Clean up the database after each test
        self.clean_database()

    def init_database(self):
        # Connect to the database and create tables
        conn = connect_db()
        cursor = conn.cursor()

        # Drop tables if they exist
        cursor.execute('DROP TABLE IF EXISTS tasks')
        cursor.execute('DROP TABLE IF EXISTS users')

        # Re-initialize tables
        Task.init_table()
        User.init_table()  # Placeholder for user table initialization

        conn.commit()
        conn.close()

    def clean_database(self):
        # Remove data from tables after each test
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks')
        cursor.execute('DELETE FROM users')
        conn.commit()
        conn.close()

    # Test cases for Task APIs

    def test_create_task(self):
        # Test creating a new task
        new_task = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'Pending'
        }
        response = self.app.post('/tasks', data=json.dumps(new_task), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], new_task['title'])
        self.assertEqual(data['status'], new_task['status'])

    def test_get_all_tasks(self):
        # Test retrieving all tasks
        # First, create a task
        self.test_create_task()
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) >= 1)

    def test_get_task_by_id(self):
        # Test retrieving a single task by ID
        # First, create a task
        self.test_create_task()
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'Test Task')

    def test_update_task(self):
        # Test updating an existing task
        self.test_create_task()
        updated_task = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'Completed'
        }
        response = self.app.put('/tasks/1', data=json.dumps(updated_task), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Verify the update
        get_response = self.app.get('/tasks/1')
        data = json.loads(get_response.data)
        self.assertEqual(data['title'], updated_task['title'])
        self.assertEqual(data['status'], updated_task['status'])

    def test_delete_task(self):
        # Test deleting a task
        self.test_create_task()
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        # Verify deletion
        get_response = self.app.get('/tasks/1')
        self.assertEqual(get_response.status_code, 404)

    def test_task_not_found(self):
        # Test getting a non-existent task
        response = self.app.get('/tasks/999')
        self.assertEqual(response.status_code, 404)

    # Placeholder test cases for User APIs

    def test_create_user(self):
        # Placeholder: Test creating a new user
        response = self.app.post('/users', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 501)  # Not Implemented

    def test_get_user(self):
        # Placeholder: Test retrieving a user
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 501)  # Not Implemented

    def test_update_user(self):
        # Placeholder: Test updating a user
        response = self.app.put('/users/1', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 501)  # Not Implemented

    def test_delete_user(self):
        # Placeholder: Test deleting a user
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 501)  # Not Implemented

if __name__ == '__main__':
    unittest.main()