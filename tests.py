import unittest
from playhouse.test_utils import test_database

from peewee import *

from app import app
from models import Todo, User

# Database in memory
DB = SqliteDatabase(':memory:')


class BaseTest(unittest.TestCase):
    """Base class"""
    def setUp(self):
        """setUp method
        - defining app
        - connect to database
        - create tables
        """
        app.config['TESTING'] = True
        self.app = app.test_client()

        DB.connect()
        DB.create_tables([User, Todo], safe=True)

    def tearDown(self):
        """tearDown method
        - delete tables
        - close database
        """
        DB.drop_tables(User, Todo)
        DB.close()


class ModelResourcesTest(BaseTest):
    """Model test class"""

    # data for user creation
    data = {
            'username': 'test_1',
            'email': 'example@mail.com',
            'password': 'password',
            'verify_password': 'password'
        }

    @staticmethod
    def create_user(prefix=None):
        """create user method
        - creates an user with the 'prefix' parameter"""
        User.create_user(
            username=f'{prefix}_user',
            email=f'example_{prefix}@mail.com',
            password='password'
        )

    def test_create_user(self):
        """user create test
        - test length of User objects, max_value should be 1
        - test username
        - test status code when user is created
        """
        with test_database(DB, (User, )):
            self.create_user('test_1')
            self.assertEqual(len(User.select()), 1)
            response = self.app.get('/api/v1/users')
            self.assertEqual(User.select().get().username, 'test_1_user')
            self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        """new user create test
        - test status code when user is created
        """
        with test_database(DB, (User,)):
            response = self.app.post('/api/v1/users', data=self.data)
            self.assertEqual(response.status_code, 201)

    def test_create_todo(self):
        """todo create test
        - test length of Todo objects, max_value should be 1
        - test status code when user is created
        """
        with test_database(DB, (Todo,)):
            self.create_user('test_2')
            user = User.select().get()
            Todo.create(name='Walk Tomika', created_by=user.id)
            self.assertEqual(len(Todo.select()), 1)
            response = self.app.post('/api/v1/todos')
            self.assertEqual(response.status_code, 200)


class ViewTest(BaseTest):
    """View test class"""
    def test_my_todos(self):
        """todo test
        - test status code
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
