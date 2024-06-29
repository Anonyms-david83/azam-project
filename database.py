import sqlite3

def create_connection():
    return sqlite3.connect('users.db')

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            gender TEXT,
            city TEXT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS friend_requests (
            user_id INTEGER,
            friend_id INTEGER,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(friend_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_role_column():
    conn = create_connection()
    c = conn.cursor()
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]
    if 'role' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        conn.commit()
    conn.close()

def is_username_taken(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_user(first_name, last_name, birth_date, gender, city, username, password, role):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (first_name, last_name, birth_date, gender, city, username, password, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, birth_date, gender, city, username, password, role))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user_data = c.fetchone()
    conn.close()
    return user_data

def get_user_by_username(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data

def get_user_by_id(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id=?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result


def add_friend(user_id, friend_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
    conn.commit()
    conn.close()

def get_friends(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT friend_id FROM friends WHERE user_id=?', (user_id,))
    friends = c.fetchall()
    conn.close()
    return friends

def send_message(sender_id, receiver_id, content):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)', (sender_id, receiver_id, content))
    conn.commit()
    conn.close()

def get_received_messages(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE receiver_id=? ORDER BY timestamp', (user_id,))
    messages = c.fetchall()
    conn.close()
    return messages

def get_sent_messages(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE sender_id=? ORDER BY timestamp', (user_id,))
    messages = c.fetchall()
    conn.close()
    return messages

def create_post(user_id, content):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)', (user_id, content))
    conn.commit()
    conn.close()

def get_posts(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE user_id=? ORDER BY timestamp', (user_id,))
    posts = c.fetchall()
    conn.close()
    return posts

def get_all_users():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

def get_all_posts():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    conn.close()
    return posts

def delete_post(post_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id=?', (post_id,))
    conn.commit()
    rowcount = c.rowcount
    conn.close()
    return rowcount > 0

def get_all_friend_requests():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT user_id, friend_id FROM friend_requests')
    requests = c.fetchall()
    conn.close()
    return requests

def send_friend_request(user_id, friend_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO friend_requests (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
    conn.commit()
    conn.close()

def get_incoming_friend_requests(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT user_id FROM friend_requests WHERE friend_id=? AND status="pending"', (user_id,))
    requests = c.fetchall()
    conn.close()
    return requests

def accept_friend_request(user_id, friend_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM friend_requests WHERE user_id=? AND friend_id=?', (friend_id, user_id))
    c.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
    conn.commit()
    conn.close()

def decline_friend_request(user_id, friend_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM friend_requests WHERE user_id=? AND friend_id=?', (friend_id, user_id))
    conn.commit()
    conn.close()

def get_accepted_friends(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT f.friend_id, u.username FROM friends f INNER JOIN users u ON f.friend_id = u.id WHERE f.user_id=?', (user_id,))
    result = c.fetchall()
    conn.close()
    return result
    

create_table()
add_role_column()
