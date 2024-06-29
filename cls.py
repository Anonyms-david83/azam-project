from datetime import datetime
import database

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def is_valid(self):
        try:
            datetime(self.year, self.month, self.day)
            return True
        except ValueError:
            return False

class User:
    def __init__(self, user_id, first_name, last_name, birth_date, gender, city, username, password, role='user'):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.city = city
        self.username = username
        self.password = password
        self.role = role

    @classmethod
    def is_username_taken(cls, username):
        return database.is_username_taken(username)

    def save_to_db(self):
        database.save_user(self.first_name, self.last_name, self.birth_date, self.gender, self.city, self.username, self.password, self.role)

    @classmethod
    def authenticate(cls, username, password):
        user_data = database.authenticate_user(username, password)
        if user_data:
            return cls(*user_data)
        return None

    @classmethod
    def get_by_username(cls, username):
        user_data = database.get_user_by_username(username)
        if user_data:
            return cls(*user_data)
        return None

    @classmethod
    def get_by_id(cls, user_id):
        user_data = database.get_user_by_id(user_id)
        if user_data:
            return cls(*user_data)
        return None

    def send_friend_request(self, friend_username):
        friend = User.get_by_username(friend_username)
        if friend:
            database.send_friend_request(self.id, friend.id)
            return True
        return False

    def send_message(self, receiver_username, message):
        receiver = User.get_by_username(receiver_username)
        if receiver:
            database.send_message(self.id, receiver.id, message)
            return True
        return False

    def create_post(self, content):
        database.create_post(self.id, content)

    def get_friends(self):
        return database.get_friends(self.id)

    def get_posts(self, user_id=None):
        if user_id is None:
            user_id = self.id
        return database.get_posts(user_id)

    def get_received_messages(self):
        return database.get_received_messages(self.id)

    def get_sent_messages(self):
        return database.get_sent_messages(self.id)

    @classmethod
    def get_all_users(cls):
        return database.get_all_users()

    @classmethod
    def get_all_posts(cls):
        return database.get_all_posts()

    @classmethod
    def delete_post_by_id(cls, post_id):
        return database.delete_post(post_id)

    @classmethod
    def get_all_friend_requests(cls):
        return database.get_all_friend_requests()

    def get_pending_friend_requests(self):
        return database.get_incoming_friend_requests(self.id)
    
    def accept_friend_request(self, friend_id):
        database.accept_friend_request(self.id, friend_id)

    def decline_friend_request(self, friend_id):
        database.decline_friend_request(self.id, friend_id)

    def get_accepted_friends(self):
        friends_data = database.get_accepted_friends(self.id)
        return friends_data
