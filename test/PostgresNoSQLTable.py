from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient
from test import TEST_HOST, TEST_TABLE, TEST_DATABASE, RELATIONAL_FIELDS, JSON_DATA, TEST_RELATIONAL_TABLE

import unittest


class PostgresNoSQLTable(unittest.TestCase):
    def setUp(self):
        self.client = PostgresNoSQLClient(host=TEST_HOST)
        self.database = self.client.create_database(TEST_DATABASE)
        self.table = self.database.create_table(TEST_TABLE)
        self.relational_table = self.database.create_table(TEST_RELATIONAL_TABLE, **RELATIONAL_FIELDS)

        # fill table
        self.first = self.table.put(JSON_DATA)

    def tearDown(self):
        # cleanup
        if self.database is not None:
            self.database.close()

        if self.client.database_exists(self.database.name):
            self.client.drop_database(self.database.name)

        # self.relational_table = None
        # self.table = None
        self.database = None
        self.client = None

    def test_get_json_field(self):
        record = self.table.get(self.first)
        self.assertEqual('blue', record.json['color'])

    def test_get_empty_record(self):
        record = self.table.get(self.first+1)
        self.assertEqual(None, record)


if __name__ == '__main__':
    unittest.main()
