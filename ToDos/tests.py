from django.test import Client, TestCase
from ToDoList import config
from ToDoList.helpers import db_operations as db_op
from ToDoList.helpers import auth_operations as auth_op


class TodoListPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        data = {
            'FirstName': 'fname', 'LastName': 'lname', 'Email': 'email',
            'Password': 'password', 'ConfirmPassword': 'password'
        }
        self.client.post(config.SIGNUP_REDIRECT_URL, data=data)

    def test_todo_list_page_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        response = self.client.get(config.TODO_LISTS_REDIRECT_URL)
        self.assertTemplateUsed(response, config.TODO_LISTS_PAGE)

    def test_todo_list_page_without_authentication(self):
        response = self.client.get(config.TODO_LISTS_REDIRECT_URL)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_tasks_page_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        response = self.client.get(config.TASKS_REDIRECT_URL+'/1')
        self.assertTemplateUsed(response, config.TASKS_PAGE)

    def test_tasks_page_without_authentication(self):
        response = self.client.get(config.TASKS_REDIRECT_URL)
        self.assertEqual(response.status_code, 404)

    def test_create_todo_list_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        response = self.client.post('/todos/create_todo_list', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/todos/todo_lists')

    def test_create_todo_list_without_authentication(self):
        data = {'ListName': 'list1'}
        response = self.client.post('/todos/create_todo_list', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_update_todo_list_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'NewName': 'list2', 'ToDoListID': '1'}
        response = self.client.post('/todos/update_todo_list', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/todos/todo_lists')

    def test_update_todo_list_without_authentication(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        self.client.post('/users/logout')
        data = {'NewName': 'list2', 'ToDoListID': '0'}
        response = self.client.post('/todos/update_todo_list', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_delete_todo_list_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1'}
        response = self.client.post('/todos/delete_todo_list', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/todos/todo_lists')

    def test_delete_todo_list_without_authentication(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        self.client.post('/users/logout')
        data = {'ToDoListID': '0'}
        response = self.client.post('/todos/delete_todo_list', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_get_tasks_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        response = self.client.get('/todos/get_tasks/1', data=data)
        self.assertTemplateUsed(response, config.TASKS_PAGE)

    def test_get_tasks_without_authentication(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        self.client.post('/users/logout')
        response = self.client.get('/todos/get_tasks/1', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_create_task_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        response = self.client.post('/todos/create_task', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, config.TASKS_REDIRECT_URL+'/1')

    def test_create_task_without_authentication(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/users/logout')
        response = self.client.post('/todos/create_task', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_update_task_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        data = {'ToDoListID': '1', 'NewTaskValue': 'task2', 'TaskID': 1}
        response = self.client.post('/todos/update_task', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, config.TASKS_REDIRECT_URL+'/1')

    def test_update_task_without_authentication(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        self.client.post('/users/logout')
        data = {'ToDoListID': '1', 'NewTaskValue': 'task2', 'TaskID': 1}
        response = self.client.post('/todos/update_task', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_delete_task_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        data = {'ToDoListID': '1', 'TaskID': 1}
        response = self.client.post('/todos/delete_task', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, config.TASKS_REDIRECT_URL+'/1')

    def test_delete_task_without_authentication(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        self.client.post('/users/logout')
        data = {'ToDoListID': '1', 'TaskID': 1}
        response = self.client.post('/todos/delete_task', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')

    def test_toggle_task_status_authenticated(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        data = {'ToDoListID': '1', 'TaskID': 1}
        response = self.client.post('/todos/toggle_task_status', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, config.TASKS_REDIRECT_URL+'/1')

    def test_toggle_task_status_without_authentication(self):
        data = {'Email': 'email', 'Password': 'password'}
        self.client.post(config.LOGIN_REDIRECT_URL, data=data)
        data = {'ListName': 'list1'}
        self.client.post('/todos/create_todo_list', data=data)
        data = {'ToDoListID': '1', 'TaskValue': 'task1'}
        self.client.post('/todos/create_task', data=data)
        self.client.post('/users/logout')
        data = {'ToDoListID': '1', 'TaskID': 1}
        response = self.client.post('/todos/toggle_task_status', data=data)
        # redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/login')
