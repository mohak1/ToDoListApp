"""This file contains unit tests for functions in `validator.py`"""

import unittest

from ToDoList.helpers import custom_exceptions as ce
from ToDoList.helpers import validator


class TestValidator(unittest.TestCase):

    def test_check_signup_params_length_no_error(self):
        data = {
            'FirstName': 'fname', 'LastName': 'lname',
            'Email': 'email', 'Password': 'password'
        }
        validator.check_signup_params_length(data)

    def test_check_signup_params_length_error_raised(self):
        data = {
            'FirstName': '', 'LastName': 'lname',
            'Email': 'email', 'Password': 'password'
        }
        with self.assertRaises(ce.UnexpectedLengthError):
            validator.check_signup_params_length(data)

    def test_check_name_length_no_error(self):
        validator.check_name_length('somestring')

    def test_check_name_length_error_raised(self):
        with self.assertRaises(ce.UnexpectedLengthError):
            validator.check_name_length('')

    def test_check_email_length_no_error(self):
        validator.check_email_length('somestring')

    def test_check_email_length_error_raised(self):
        with self.assertRaises(ce.UnexpectedLengthError):
            validator.check_email_length('')

    def test_check_password_length_no_error(self):
        validator.check_password_length('somestring')

    def test_check_password_length_error_raised(self):
        with self.assertRaises(ce.UnexpectedLengthError):
            validator.check_password_length('')

    def test_check_required_params_no_error(self):
        required = ['FirstName', 'LastName']
        params = data = {'FirstName': 'a', 'LastName': 'b'}
        validator.check_required_params(params, required)

    def test_check_required_params_error_raised(self):
        required = ['FirstName', 'LastName', 'Email', 'Password']
        params = data = {'FirstName': 'a', 'LastName': 'b'}
        with self.assertRaises(ce.InvalidRequestParamsError):
            validator.check_required_params(params, required)
