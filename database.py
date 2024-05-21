import sqlite3

# Database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

def create_connection():
    return sqlite3.connect('users.db')

# Create table for users
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            gender TEXT,
            city TEXT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            user_id INTEGER,
            friend_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(friend_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()

def is_username_taken(username):
    c.execute('SELECT username FROM users WHERE username=?', (username,))
    return c.fetchone() is not None

def save_user(first_name, last_name, birth_date, gender, city, username, password):
    c.execute('''
        INSERT INTO users (first_name, last_name, birth_date, gender, city, username, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, birth_date, gender, city, username, password))
    conn.commit()

def authenticate_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    return c.fetchone()

def get_user_by_username(username):
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    return c.fetchone()

def add_friend(user_id, friend_id):
    c.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
    conn.commit()

def get_friends(user_id):
    c.execute('SELECT friend_id FROM friends WHERE user_id=?', (user_id,))
    return c.fetchall()

def send_message(sender_id, receiver_id, content):
    c.execute('INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)', (sender_id, receiver_id, content))
    conn.commit()

def get_messages(user_id):
    c.execute('SELECT * FROM messages WHERE sender_id=? OR receiver_id=? ORDER BY timestamp', (user_id, user_id))
    return c.fetchall()

def create_post(user_id, content):
    c.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()

def get_posts(user_id):
    c.execute('SELECT * FROM posts WHERE user_id=? ORDER BY timestamp', (user_id,))
    return c.fetchall()

def get_friend_posts(user_id):
    c.execute('''
        SELECT * FROM posts 
        WHERE user_id IN (SELECT friend_id FROM friends WHERE user_id=?)
        ORDER BY timestamp
    ''', (user_id,))
    return c.fetchall()

# Ensure the table is created when the module is imported


def send_friend_request(user_id, friend_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
    conn.commit()
    conn.close()


create_table()
