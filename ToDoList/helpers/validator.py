"""This file contains methods for data validation"""

import typing as ty

from django.http.request import QueryDict

from ToDoList import config
from ToDoList.helpers import custom_exceptions as ce


def check_name_length(name: str):
    if len(name) < 1:
        raise ce.UnexpectedLengthError('Name value cannot be empty')
    if len(name) > config.MAX_NAME_LENGTH:
        raise ce.UnexpectedLengthError(
            'Name length should be less than '
            f'`{config.MAX_NAME_LENGTH}` characters'
        )

def check_email_length(email):
    if len(email) < 1:
        raise ce.UnexpectedLengthError('Email value cannot be empty')
    if len(email) > config.MAX_EMAIL_LENGTH:
        raise ce.UnexpectedLengthError(
            'Email length should be less than '
            f'`{config.MAX_EMAIL_LENGTH}` characters'
        )

def check_password_length(passw):
    if len(passw) < 1:
        raise ce.UnexpectedLengthError('Password value cannot be empty')
    if len(passw) > config.MAX_NAME_LENGTH:
        raise ce.UnexpectedLengthError(
            'Password length should be less than '
            f'`{config.MAX_PASSWORD_LENGTH}` characters'
        )

def check_required_params(params: QueryDict, required: ty.List):
    missing_params = []
    for i in required:
        if params.get(i) is None:
            missing_params.append(i)
    if missing_params:
        raise ce.InvalidRequestParamsError(
            f'Missing required params: {missing_params}'
        )
