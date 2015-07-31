from pg4nosql import DEFAULT_POSTGRES_HOST, DEFAULT_POSTGRES_DATABASE, DEFAULT_POSTGRES_PORT
from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient
import unittest
from test import TEST_DB_HOST, TEST_DATABASE, TEST_TEMP_DATABASE, TEST_DB_USER, TEST_DB_PASSWORD


class PostgresNoSQLClientTest(unittest.TestCase):

    def setUp(self):
        self.client = PostgresNoSQLClient(host=TEST_DB_HOST, user=TEST_DB_USER, password=TEST_DB_PASSWORD)
        self.database = self.client.create_database(TEST_DATABASE)
        self.temp_db = None

    def tearDown(self):
        # cleanup
        if self.temp_db is not None:
            self.temp_db.close()

        if self.database is not None:
            self.database.close()

        if self.client.database_exists(TEST_TEMP_DATABASE):
            self.client.drop_database(TEST_TEMP_DATABASE)

        if self.client.database_exists(self.database.name):
            self.client.drop_database(self.database.name)

        self.database = None
        self.temp_db = None
        self.client = None

    def test_init_without_parameter(self):
        client = PostgresNoSQLClient()
        self.assertEqual(DEFAULT_POSTGRES_HOST, client.host)
        self.assertEqual(DEFAULT_POSTGRES_PORT, client.port)
        self.assertEqual(DEFAULT_POSTGRES_DATABASE, client.database)

    def test_init_with_parameter(self):
        client = PostgresNoSQLClient(host='test', port=2000, database='my_test', user='hello', password='world')
        self.assertEqual('test', client.host)
        self.assertEqual(2000, client.port)
        self.assertEqual('my_test', client.database)

    def test_create_database(self):
        self.temp_db = self.client.create_database(TEST_TEMP_DATABASE)
        self.assertEqual(TEST_TEMP_DATABASE, self.temp_db.name)
        self.assertNotEqual(None, self.temp_db.connection, 'no connection established')

    def test_database_exists(self):
        self.assertEqual(True, self.client.database_exists(TEST_DATABASE))
        self.assertEqual(False, self.client.database_exists(TEST_DATABASE+'12345'))

    def test_drop_database(self):
        self.temp_db = self.client.create_database(TEST_TEMP_DATABASE)
        self.temp_db.close()
        self.client.drop_database(TEST_TEMP_DATABASE)
        self.assertEqual(False, self.client.database_exists(TEST_TEMP_DATABASE))

    def test_get_database_with_existing(self):
        self.temp_db = self.client.get_database(TEST_DATABASE)
        self.assertEqual(TEST_DATABASE, self.temp_db.name)
        self.assertNotEqual(None, self.temp_db.connection, 'no connection established')

    def test_get_database_without_existing(self):
        self.temp_db = self.client.get_database(TEST_DATABASE+'12345')
        self.assertEqual(None, self.temp_db, 'there should be no database')

    def test_get_or_create_with_existing(self):
        self.temp_db = self.client.get_or_create_database(TEST_DATABASE)
        self.assertEqual(TEST_DATABASE, self.temp_db.name)

    def test_get_or_create_without_existing(self):
        self.temp_db = self.client.get_or_create_database(TEST_TEMP_DATABASE)
        self.assertEqual(TEST_TEMP_DATABASE, self.temp_db.name)

if __name__ == '__main__':
    unittest.main()
