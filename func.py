from art import *

##############################[initializing fuctions]##################################
def start_app():
    art1 = text2art("Welcome", font='block',chr_ignore=True)
    print(art1)
    choose = input("Choose Your Login Method ... \n 1)Login \n 2)Signup \n 3)Exit \n ==>")

    match choose:
        case '1':
            login()
        case '2':
            signup()
        case '3':
           app_exit()

##############################[authentication functions]##################################

def signup():
    pass

def login():
    pass

def app_exit():
    exit()

#############################

