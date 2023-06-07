"""This file contains methods for data validation"""

import typing as ty

from django.http.request import QueryDict

from ToDoList import config
from ToDoList.helpers import custom_exceptions as ce
from ToDoList.helpers import decorators


@decorators.log_method
def check_signup_params_length(params: QueryDict) -> None:
    """
    Ensures that the length of FirstName, LastName, Email and Password
    is greater than 0 and less than maximum allowed length
    Raises `ce.UnexpectedLengthError` if length is out of expected range
    """
    check_name_length(params.get('FirstName'))
    check_name_length(params.get('LastName'))
    check_email_length(params.get('Email'))
    check_password_length(params.get('Password'))

@decorators.log_method
def check_name_length(name: str) -> None:
    """
    Verifies that name length is greater than 0 and less than
    maximum allowed name length
    Raises `ce.UnexpectedLengthError` if length is out of expected range
    """
    if len(name) < 1:
        raise ce.UnexpectedLengthError('Name value cannot be empty')
    if len(name) > config.MAX_NAME_LENGTH:
        raise ce.UnexpectedLengthError(
            'Name length should be less than '
            f'`{config.MAX_NAME_LENGTH}` characters'
        )

@decorators.log_method
def check_email_length(email: str) -> None:
    """
    Verifies that email length is greater than 0 and less than
    maximum allowed email length
    Raises `ce.UnexpectedLengthError` if length is out of expected range
    """
    if len(email) < 1:
        raise ce.UnexpectedLengthError('Email value cannot be empty')
    if len(email) > config.MAX_EMAIL_LENGTH:
        raise ce.UnexpectedLengthError(
            'Email length should be less than '
            f'`{config.MAX_EMAIL_LENGTH}` characters'
        )

@decorators.log_method
def check_todo_list_name_length(name: str) -> None:
    """
    Verifies that the name length of ToDo List is longer than 0 and less
    than maximum allowed length
    Raises `ce.UnexpectedLengthError` if length is out of expected range
    """
    if len(name) < 1:
        raise ce.UnexpectedLengthError('ToDo ListName cannot be empty')
    if len(name) > config.MAX_LIST_NAME_LENGTH:
        raise ce.UnexpectedLengthError(
            'ToDo ListName length should be less than '
            f'`{config.MAX_LIST_NAME_LENGTH}` characters'
        )

@decorators.log_method
def check_password_length(passw: str) -> None:
    """
    Verifies that password length is greater than 0 and less than
    maximum allowed password length
    Raises `ce.UnexpectedLengthError` if length is out of expected range
    """
    if len(passw) < 1:
        raise ce.UnexpectedLengthError('Password value cannot be empty')
    if len(passw) > config.MAX_NAME_LENGTH:
        raise ce.UnexpectedLengthError(
            'Password length should be less than '
            f'`{config.MAX_PASSWORD_LENGTH}` characters'
        )

@decorators.log_method
def check_required_params(params: QueryDict, required: ty.List) -> None:
    """
    Verifies that items in `required` are present in `params`
    Raises `ce.InvalidRequestParamsError` if some values are missing
    """
    missing_params = []
    for i in required:
        if params.get(i) is None:
            missing_params.append(i)
    if missing_params:
        raise ce.InvalidRequestParamsError(
            f'Missing required params: {missing_params}'
        )
