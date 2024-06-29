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

def logout_user():
    print("Logging out...")
    start_app()

def show_menu(user):
    while True:
        print("\nMenu:")
        print("1) Send Friend Request")
        print("2) Send Message")
        print("3) Create New Post")
        print("4) View Posts of Others")
        print("5) View Previous Messages")
        print("6) View Previous Posts")
        print("7) Logout")

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
                logout_user()
                return
            case _:
                print("Invalid choice. Please try again.")

def show_admin_menu(user):
    while True:
        print("\nAdmin Menu:")
        print("1) View All Users")
        print("2) View All Posts")
        print("3) Delete Post")
        print("4) View Friend Requests")
        print("5) Logout")

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
                logout_user()
                return
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
    friend_user = User.get_user_by_username(friend_username)
    if friend_user:
        user.send_friend_request(friend_user[0])  # Assuming user ID is at index 0
        print("Friend request sent!")
    else:
        print("User not found.")

def send_message(user):
    print("Send Message")
    recipient_username = input("Enter recipient's username: ")
    recipient_user = User.get_by_username(recipient_username)
    if recipient_user:
        message = input("Enter your message: ")
        user.send_message(recipient_user.id, message)  # Assuming user ID is stored in recipient_user.id
        print("Message sent!")
    else:
        print("User not found.")

def create_post(user):
    print("Create New Post")
    content = input("Enter your post content: ")
    user.create_post(content)
    print("Post created!")

def view_posts_of_others(user):
    print("View Posts of Others")
    posts = User.get_all_posts()
    for post in posts:
        print(f"User ID: {post[1]}, Content: {post[2]}, Timestamp: {post[3]}")

def view_previous_messages(user):
    print("View Previous Messages")
    messages = user.get_messages()
    for message in messages:
        print(f"From: {message[1]}, To: {message[2]}, Content: {message[3]}, Timestamp: {message[4]}")

def view_previous_posts(user):
    print("View Previous Posts")
    posts = user.get_posts()
    for post in posts:
        print(f"Content: {post[2]}, Timestamp: {post[3]}")
