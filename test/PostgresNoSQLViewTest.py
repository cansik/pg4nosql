import unittest

from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient
from __init__ import TEST_DB_HOST, TEST_DATABASE, TEST_DB_USER, TEST_DB_PASSWORD


class PostgresNoSQLViewTest(unittest.TestCase):
    def setUp(self):
        self.client = PostgresNoSQLClient(host=TEST_DB_HOST, user=TEST_DB_USER, password=TEST_DB_PASSWORD)

        # pre cleanup
        if self.client.database_exists(TEST_DATABASE):
            self.client.drop_database(TEST_DATABASE)

        self.database = self.client.create_database(TEST_DATABASE)
        self.user = self.database.create_table('users', name='text')
        self.info = self.database.create_table('info', fk_user='int references users(id)', age='integer')

        # fill table with data
        self.user.insert(name='Simon')
        self.user.insert(name='Felix')
        self.info.insert(fk_user=1, age=30)
        self.info.insert(fk_user=2, age=40)

        # create view
        self.database.execute('CREATE VIEW user_view AS SELECT users.name, info.age FROM users JOIN info ON users.id = info.fk_user')

        # get view
        self.user_view = self.database.get_view('user_view')

    def tearDown(self):
        # cleanup
        if self.database is not None:
            self.database.close()

        if self.client.database_exists(self.database.name):
            self.client.drop_database(self.database.name)

    def test_query_view(self):
        records = self.user_view.query()
        self.assertEqual(2, len(records))

if __name__ == '__main__':
    unittest.main()
