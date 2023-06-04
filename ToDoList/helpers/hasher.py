from django.contrib.auth.hashers import check_password, make_password

from ToDoList import config


def get_hash(password):
    hashed_password = make_password(password, salt=config.SALT)
    return hashed_password

def verify_password(password, hashed_password):
    return check_password(password, hashed_password)
