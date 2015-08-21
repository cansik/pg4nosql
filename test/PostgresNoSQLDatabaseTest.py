from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient
from __init__ import TEST_DB_HOST, TEST_DATABASE, TEST_TEMP_DATABASE, TEST_TABLE, TEST_TEMP_TABLE, RELATIONAL_FIELDS, \
    TEST_DB_USER, TEST_DB_PASSWORD

__author__ = 'cansik'

import unittest


class PostgresNoSQLDatabaseTest(unittest.TestCase):

    def setUp(self):
        self.client = PostgresNoSQLClient(host=TEST_DB_HOST, user=TEST_DB_USER, password=TEST_DB_PASSWORD)

        # pre cleanup
        if self.client.database_exists(TEST_DATABASE):
            self.client.drop_database(TEST_DATABASE)

        self.database = self.client.create_database(TEST_DATABASE)
        self.table = self.database.create_table(TEST_TABLE)

    def tearDown(self):
        # cleanup
        if self.database is not None:
            self.database.close()

        if self.client.database_exists(self.database.name):
            self.client.drop_database(self.database.name)

        self.database = None
        self.table = None
        self.client = None

    def test_table_exists(self):
        self.assertEqual(True, self.database.table_exists(TEST_TABLE))
        self.assertEqual(False, self.database.table_exists(TEST_TABLE+'12345'))

    def test_get_table_with_existing(self):
        self.assertNotEqual(None, self.database.get_table(TEST_TABLE))

    def test_get_table_without_existing(self):
        self.assertEqual(None, self.database.get_table(TEST_TABLE+'12345'))

    def test_create_table(self):
        temp = self.database.create_table(TEST_TEMP_TABLE)
        self.assertEqual(TEST_TEMP_TABLE, temp.name)

    def test_create_table_with_bigserial(self):
        temp = self.database.create_table(TEST_TEMP_TABLE, row_identifier_type='BIGSERIAL')
        self.assertEqual(TEST_TEMP_TABLE, temp.name)

    def test_create_table_with_relational_fields(self):
        temp = self.database.create_table(TEST_TEMP_TABLE, **RELATIONAL_FIELDS)
        self.assertEqual(TEST_TEMP_TABLE, temp.name)

    def test_drop_table(self):
        self.database.drop_table(TEST_TABLE)
        self.assertEqual(False, self.database.table_exists(TEST_TABLE))

    def test_get_or_create_table_with_existing(self):
        temp = self.database.get_or_create_table(TEST_TABLE)
        self.assertEqual(TEST_TABLE, temp.name)

    def test_get_or_create_table_without_existing(self):
        temp = self.database.get_or_create_table(TEST_TEMP_TABLE)
        self.assertEqual(TEST_TEMP_TABLE, temp.name)


if __name__ == '__main__':
    unittest.main()
