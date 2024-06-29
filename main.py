import database
from func import start_app

def initialize_database():
    database.create_table()
    database.add_role_column()

if __name__ == "__main__":
    initialize_database()
    start_app()
