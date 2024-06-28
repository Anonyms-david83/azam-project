from art import text2art
from cls import Date, User

##############################[initializing fuctions]##################################
def start_app():
    art1 = text2art("Welcome", font='block', chr_ignore=True)
    print(art1)
    choose = input("Choose Your Login Method ... \n 1)Login \n 2)Signup \n 3)Admin Login \n 4)Admin Signup \n 5)Exit \n ==>")

    match choose:
        case '1':
            login_user()
        case '2':
            register_user()
        case '3':
            admin_login()
        case '4':
            register_admin()
        case '5':
            app_exit()

##############################[authentication functions]##################################

def app_exit():
    exit()

def register_user():
    print("Registration Form")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    while True:
        year = int(input("Birth Year: "))
        month = int(input("Birth Month: "))
        day = int(input("Birth Day: "))
        birth_date = Date(year, month, day)
        if birth_date.is_valid():
            birth_date_str = f"{year}-{month:02d}-{day:02d}"
            break
        else:
            print("Invalid date. Please enter again.")

    gender = input("Gender: ")
    city = input("City: ")

    while True:
        username = input("Username: ")
        if not User.is_username_taken(username):
            break
        else:
            print("Username is already taken. Please choose another one.")

    password = input("Password: ")

    new_user = User(None, first_name, last_name, birth_date_str, gender, city, username, password)
    new_user.save_to_db()
    print("Registration successful! Redirecting to login...")
    login_user()

def register_admin():
    print("Admin Registration Form")
    referral_code = input("Enter referral code: ")
    if referral_code != "farokhadmin":
        print("Invalid referral code. Access denied.")
        return

    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    while True:
        year = int(input("Birth Year: "))
        month = int(input("Birth Month: "))
        day = int(input("Birth Day: "))
        birth_date = Date(year, month, day)
        if birth_date.is_valid():
            birth_date_str = f"{year}-{month:02d}-{day:02d}"
            break
        else:
            print("Invalid date. Please enter again.")

    gender = input("Gender: ")
    city = input("City: ")

    while True:
        username = input("Username: ")
        if not User.is_username_taken(username):
            break
        else:
            print("Username is already taken. Please choose another one.")

    password = input("Password: ")

    new_admin = User(None, first_name, last_name, birth_date_str, gender, city, username, password, role='admin')
    new_admin.save_to_db()
    print("Admin registration successful! Redirecting to login...")
    admin_login()

def login_user():
    while True:
        print("Login (type 'exit' to quit)")
        username = input("Username: ")
        if username.lower() == 'exit':
            print("Exiting login...")
            return

        password = input("Password: ")
        if password.lower() == 'exit':
            print("Exiting login...")
            return

        user = User.authenticate(username, password)
        if user:
            print("Login successful!")
            show_menu(user)
            return
        else:
            print("Invalid username or password. Please try again or type 'exit' to quit.")

def admin_login():
    while True:
        print("Admin Login (type 'exit' to quit)")
        username = input("Username: ")
        if username.lower() == 'exit':
            print("Exiting login...")
            return

        password = input("Password: ")
        if password.lower() == 'exit':
            print("Exiting login...")
            return

        user = User.authenticate(username, password)
        if user and user.role == 'admin':
            print("Admin login successful!")
            show_admin_menu(user)
            return
        else:
            print("Invalid username or password or not an admin. Please try again or type 'exit' to quit.")

def show_menu(user):
    while True:
        print("\nMenu:")
        print("1) Send Friend Request")
        print("2) Send Message")
        print("3) Create New Post")
        print("4) View Posts of Others")
        print("5) View Previous Messages")
        print("6) View Previous Posts")
        print("7) Exit")

        choice = input("Enter your choice: ")

        match choice:
            case '1':
                send_friend_request(user)
            case '2':
                send_message(user)
            case '3':
                create_post(user)
            case '4':
                view_posts_of_others(user)
            case '5':
                view_previous_messages(user)
            case '6':
                view_previous_posts(user)
            case '7':
                print("Exiting...")
                exit()
            case _:
                print("Invalid choice. Please try again.")

def show_admin_menu(user):
    while True:
        print("\nAdmin Menu:")
        print("1) View All Users")
        print("2) View All Posts")
        print("3) Delete Post")
        print("4) View Friend Requests")
        print("5) Exit")

        choice = input("Enter your choice: ")

        match choice:
            case '1':
                view_all_users()
            case '2':
                view_all_posts()
            case '3':
                delete_post()
            case '4':
                view_friend_requests()
            case '5':
                print("Exiting...")
                exit()
            case _:
                print("Invalid choice. Please try again.")

def view_all_users():
    users = User.get_all_users()
    print("All users:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[6]}")

def view_all_posts():
    posts = User.get_all_posts()
    print("All posts:")
    for post in posts:
        print(f"Post ID: {post[0]}, User ID: {post[1]}, Content: {post[2]}, Timestamp: {post[3]}")

def delete_post():
    post_id = int(input("Enter the post ID to delete: "))
    if User.delete_post_by_id(post_id):
        print("Post deleted successfully.")
    else:
        print("Post not found.")

def view_friend_requests():
    requests = User.get_all_friend_requests()
    print("All friend requests:")
    for request in requests:
        print(f"User ID: {request[0]}, Friend ID: {request[1]}")

def send_friend_request(user):
    print("Send Friend Request")
    users = User.get_all_users()
    print("List of all users:")
    for user_tuple in users:
        print(f"ID: {user_tuple[0]}, Username: {user_tuple[6]}")  # Assuming ID is at index 0 and username at index 6

    friend_username = input("Enter username to send friend request: ")
    if User.send_friend_request(user.username, friend_username):
        print(f"Friend request sent to {friend_username}.")
    else:
        print(f"User {friend_username} not found or already a friend.")

def send_message(user):
    print("Send Message")
    receiver_username = input("Enter the username of the person you want to send a message to: ")
    message = input("Enter your message: ")

    if user.send_message(receiver_username, message):
        print(f"Message sent to {receiver_username}.")
    else:
        print(f"Failed to send message. Make sure {receiver_username} is in your friend list and the username is correct.")

def create_post(user):
    print("Create New Post")
    content = input("Enter your post content: ")
    user.create_post(content)
    print("Post created successfully.")

def view_posts_of_others(user):
    print("View Posts of Others")
    friends = user.get_friends()
    print("Your friends:")
    for friend in friends:
        print(friend[0])

    friend_username = input("Enter the username of the friend whose posts you want to view: ")
    friend = User.get_by_username(friend_username)

    if friend:
        posts = friend.get_posts()
        for post in posts:
            print(f"{post[1]}: {post[0]}")
    else:
        print(f"User {friend_username} not found.")

def view_previous_posts(user):
    print("View Previous Posts")
    posts = user.get_posts()
    if not posts:
        print("No posts found.")
    else:
        for post in posts:
            print(f"ID: {post[0]}, Content: {post[1]}, Date: {post[2]}")

def view_previous_messages(user):
    print("View Previous Messages")
    received_messages = user.get_received_messages()
    sent_messages = user.get_sent_messages()

    print("Received Messages:")
    if not received_messages:
        print("No received messages found.")
    else:
        for message in received_messages:
            print(f"ID: {message[0]}, From: {message[3]}, Date: {message[2]}, Content: {message[1]}")

    print("\nSent Messages:")
    if not sent_messages:
        print("No sent messages found.")
    else:
        for message in sent_messages:
            print(f"ID: {message[0]}, To: {message[3]}, Date: {message[2]}, Content: {message[1]}")
