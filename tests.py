import unittest
from playhouse.test_utils import test_database

from peewee import *

from app import app
from models import Todo, User


DB = SqliteDatabase(':memory:')


class BaseTest(unittest.TestCase):
    def setUp(self):
        DB.connect()
        DB.create_tables([Todo, User], safe=True)

    def tearDown(self):
        DB.drop_tables(Todo, User)
        DB.close()

class UserTestCase(BaseTest):
    ''' test cases for the user model '''
    @staticmethod # static method as it does not access anything in the class
    def create(count=2):
        ''' this test creates 2 users in the database via a function called
            create_users
        '''
        for i in range(count):
            User.create_user(
                username='user_{}'.format(i),
                email='test_{}@example.com'.format(i),
                password='password'
            )


class TodoTestCase(BaseTest, UserTestCase):
    # @staticmethod
    def create(self):
        # UserModelTestCase.create()
        # user = User.select().get()
        Todo.create(name='Walk Tomika', created_by=self.create())
        # Todo.create(name='Clean Car', created_by=user.id)

    def test_todo_create(self):
        with test_database(DB, (Todo,)):
            Todo.create(
                name='Walk Tomika', created_by=1
            )
            self.assertEqual(Todo.select().count(), 1)


if __name__ == '__main__':
    unittest.main()