from art import *
from cls import Date
from cls import User

##############################[initializing fuctions]##################################
def start_app():
    art1 = text2art("Welcome", font='block',chr_ignore=True)
    print(art1)
    choose = input("Choose Your Login Method ... \n 1)Login \n 2)Signup \n 3)Exit \n ==>")

    match choose:
        case '1':
            login_user()
        case '2':
            register_user()
        case '3':
           app_exit()

##############################[authentication functions]##################################

def app_exit():
    exit()


# Registration function
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
        if not User.get_by_username(username):
            break
        else:
            print("Username is already taken. Please choose another one.")

    password = input("Password: ")

    new_user = User(None, first_name, last_name, birth_date_str, gender, city, username, password)
    new_user.save_to_db()
    print("Registration successful! Redirecting to login...")
    login_user()


# Login function
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


# Menu function
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


def send_friend_request(user):
    print("Send Friend Request")
    # Show a list of users in the same city
    friends = user.get_friends()
    print("Users with similar city:")
    for friend in friends:
        print(friend[0])

    friend_username = input("Enter username to send friend request: ")
    if user.send_friend_request(friend_username):
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
        print(
            f"Failed to send message. Make sure {receiver_username} is in your friend list and the username is correct.")


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
