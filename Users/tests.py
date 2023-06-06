from django.test import Client, TestCase
from ToDoList import config
from ToDoList.helpers import db_operations as db_op
from ToDoList.helpers import auth_operations as auth_op

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        url = '/users/login'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Users/login.html')

    def test_post_with_missing_params(self):
        data = {}
        response = self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        self.assertTemplateUsed(response, config.LOGIN_PAGE)

    def test_post_with_incorrect_credentials(self):
        data = {'Email': '', 'Password': ''}
        response = self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        self.assertTemplateUsed(response, config.LOGIN_PAGE)

    def test_post_with_correct_credentials(self):
        # create a test account
        data = {
            'FirstName': 'fname', 'LastName': 'lname', 'Email': 'email',
            'Password': 'password', 'ConfirmPassword': 'password'
        }
        response = self.client.post(config.SIGNUP_REDIRECT_URL, data=data)
        data = {'Email': 'email', 'Password': 'password'}
        response = self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        self.assertEqual(response.status_code, 302)


class SignupTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(config.SIGNUP_REDIRECT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, config.SIGNUP_PAGE)

    def test_post_with_valid_data(self):
        data = {
            'FirstName': 'fname', 'LastName': 'lname', 'Email': 'email',
            'Password': 'password', 'ConfirmPassword': 'password'
        }
        response = self.client.post(config.SIGNUP_REDIRECT_URL, data=data)
        # verify that email and password exist in db
        password_hash = auth_op.get_hash(data['Password'])
        db_op.get_user_from_login_cred(data['Email'], password_hash)
        self.assertTemplateUsed(response, config.SIGNUP_PAGE)

    def test_post_with_missing_params(self):
        data = {
            'FirstName': 'fname', 'Email': 'email', 'Password': 'password',
        }
        response = self.client.post(config.SIGNUP_REDIRECT_URL, data=data)
        self.assertTemplateUsed(response, config.SIGNUP_PAGE)

    def test_post_with_password_mismatch(self):
        data = {
            'FirstName': 'fname', 'LastName': 'lname', 'Email': 'email',
            'Password': 'value1', 'ConfirmPassword': 'value2'
        }
        response = self.client.post(config.SIGNUP_REDIRECT_URL, data=data)
        self.assertTemplateUsed(response, config.SIGNUP_PAGE)

    def test_post_when_email_already_exists(self):
        data = {
            'FirstName': 'fname', 'LastName': 'lname', 'Email': 'email',
            'Password': 'password', 'ConfirmPassword': 'password'
        }
        response = self.client.post(config.SIGNUP_REDIRECT_URL, data=data)
        response = self.client.post(config.SIGNUP_REDIRECT_URL, data=data)
        self.assertTemplateUsed(response, config.SIGNUP_PAGE)


class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout(self):
        url = '/users/logout'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
