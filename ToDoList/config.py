"""This file contains constants that are used in the project"""

MAX_NAME_LENGTH = 256
MAX_EMAIL_LENGTH = 256
MAX_PASSWORD_LENGTH = 256
MAX_LIST_NAME_LENGTH = 50
MAX_TASK_VALUE_LENGTH = 256

SIGNUP_PAGE = 'Users/signup.html'
LOGIN_PAGE = 'Users/login.html'
TODO_LISTS_PAGE = 'ToDos/todo_lists.html'
TASKS_PAGE = 'ToDos/tasks.html'

LOGGING_LEVEL = 'INFO'
SIGNUP_SUCCESS_MESSAGE = 'Signup successful! Please login.'
LOGIN_FAIL_MESSAGE = 'Email or Password is incorrect. Please try again.'

SALT = '}g\x93\xd9~k\xee\xf3'

TODO_LISTS_REDIRECT_URL = '/todos/todo_lists'
LOGIN_REDIRECT_URL = '/users/login'
SIGNUP_REDIRECT_URL = '/users/signup'
TASKS_REDIRECT_URL = '/todos/tasks'
