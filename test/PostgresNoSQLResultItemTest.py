from pg4nosql import DEFAULT_JSON_COLUMN_NAME
from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient
from __init__ import TEST_DB_HOST, TEST_TABLE, TEST_DATABASE, RELATIONAL_FIELDS, JSON_DATA, TEST_RELATIONAL_TABLE, \
    RELATIONAL_DATA, TEST_DB_USER, TEST_DB_PASSWORD

import json
import unittest


class PostgresNoSQLResultItemTest(unittest.TestCase):
    def setUp(self):
        self.client = PostgresNoSQLClient(host=TEST_DB_HOST, user=TEST_DB_USER, password=TEST_DB_PASSWORD)

        # pre cleanup
        if self.client.database_exists(TEST_DATABASE):
            self.client.drop_database(TEST_DATABASE)

        self.database = self.client.create_database(TEST_DATABASE)
        self.table = self.database.create_table(TEST_TABLE)
        self.relational_table = self.database.create_table(TEST_RELATIONAL_TABLE, **RELATIONAL_FIELDS)

        # fill table
        self.first = self.table.put(JSON_DATA)
        self.first_relational = self.relational_table.put(JSON_DATA, **RELATIONAL_DATA)

    def tearDown(self):
        # cleanup
        if self.database is not None:
            self.database.close()

        if self.client.database_exists(self.database.name):
            self.client.drop_database(self.database.name)

    def test_json_serialize(self):
        record = self.table.get(self.first)
        # todo: useless unit test atm
        json_string = json.dumps(record.get_record())
        self.assertEqual(json.dumps(record.get_record()), json_string)

if __name__ == '__main__':
    unittest.main()
