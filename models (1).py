import sqlite3

# Database connection function
def connect_db():
    conn = sqlite3.connect('tasks.db')
    return conn

# Task Model
class Task:
    def __init__(self, id=None, title=None, description=None, status=None, assigned_to=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to = assigned_to  # Added assigned_to field

    # Create tasks table
    @staticmethod
    def init_table():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                assigned_to INTEGER,
                FOREIGN KEY (assigned_to) REFERENCES users (id)  -- Added foreign key reference
            )
        ''')
        conn.commit()
        conn.close()

    # Add a new task to the database
    def save(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, status, assigned_to)
            VALUES (?, ?, ?, ?)
        ''', (self.title, self.description, self.status, self.assigned_to))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()
        return self

    # Get all tasks from the database
    @staticmethod
    def get_all():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        conn.close()

        return [Task(id=row[0], title=row[1], description=row[2], status=row[3], assigned_to=row[4]) for row in tasks]

    # Get a task by ID
    @staticmethod
    def get_by_id(task_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Task(id=row[0], title=row[1], description=row[2], status=row[3], assigned_to=row[4])
        else:
            return None

    # Update a task in the database
    def update(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks SET title = ?, description = ?, status = ?, assigned_to = ?
            WHERE id = ?
        ''', (self.title, self.description, self.status, self.assigned_to, self.id))
        conn.commit()
        conn.close()

    # Delete a task from the database
    @staticmethod
    def delete(task_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

# User Model
class User:
    def __init__(self, id=None, username=None, email=None, password=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    # Create users table
    @staticmethod
    def init_table():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    # Add a new user to the database
    def save(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (self.username, self.email, self.password))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    # Get a user by ID
    @staticmethod
    def get_by_id(user_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(id=row[0], username=row[1], email=row[2], password=row[3])
        else:
            return None

    # Get all users
    @staticmethod
    def get_all():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()

        return [User(id=row[0], username=row[1], email=row[2], password=row[3]) for row in users]

    # Placeholder for user deletion and update methods
    def update(self):
        # Implement user update logic here
        pass

    @staticmethod
    def delete(user_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

# Initialize the tables
if __name__ == "__main__":
    Task.init_table()
    User.init_table()
