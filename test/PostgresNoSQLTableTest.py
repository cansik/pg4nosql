from pg4nosql import DEFAULT_JSON_COLUMN_NAME
from pg4nosql.PostgresNoSQLClient import PostgresNoSQLClient
from __init__ import TEST_DB_HOST, TEST_TABLE, TEST_DATABASE, RELATIONAL_FIELDS, JSON_DATA, TEST_RELATIONAL_TABLE, \
    RELATIONAL_DATA, TEST_DB_USER, TEST_DB_PASSWORD

import unittest


class PostgresNoSQLTableTest(unittest.TestCase):
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

    def test_get_empty_record(self):
        record = self.table.get(self.first+1)
        self.assertEqual(None, record)

    def test_get_json_field(self):
        record = self.table.get(self.first)
        self.assertEqual('blue', record.json['color'])

    def test_get_relational_field(self):
        record = self.relational_table.get(self.first_relational)
        self.assertEqual(24, record['age'])

    def test_insert(self):
        id = self.relational_table.insert(name="pascal", age=22, height=182)
        record = self.relational_table.get(id)
        self.assertEqual(22, record['age'])

    def test_put_json(self):
        id = self.table.put(JSON_DATA)
        record = self.table.get(id)
        self.assertEqual(3, record.json['items'])

    def test_put_json_with_none(self):
        id = self.table.put(None)
        record = self.table.get(id)
        self.assertEqual(None, record.get_record()[DEFAULT_JSON_COLUMN_NAME])

    def test_put_relational(self):
        id = self.relational_table.put(JSON_DATA, **RELATIONAL_DATA)
        record = self.relational_table.get(id)
        self.assertEqual(179.5, record['height'])

    def test_put_relational_without_auto_commit(self):
        id = self.relational_table.put(JSON_DATA, auto_commit=False, **RELATIONAL_DATA)
        self.relational_table.connection.rollback()
        record = self.relational_table.get(id)
        self.assertEqual(None, record)

    def test_put_relational_with_none(self):
        id = self.relational_table.put(JSON_DATA, name='florian', age=24, height=None)
        record = self.relational_table.get(id)
        self.assertEqual(None, record['height'])

    def test_update(self):
        record = self.relational_table.get(self.first_relational)
        self.relational_table.update(record.id, age=5)
        record = self.relational_table.get(self.first_relational)
        self.assertEqual(5, record['age'])

    def test_save_json(self):
        record = self.table.get(self.first)
        record.json['items'] = 15
        self.table.save(record)
        record = self.table.get(self.first)
        self.assertEqual(15, record.json['items'])

    def test_save_object_further_use(self):
        record = self.relational_table.get(self.first_relational)
        record.json['items'] = 15
        self.relational_table.save(record)
        self.assertEqual(15, record.json['items'])
        self.assertEqual('florian', record['name'])

    def test_save_json_with_none(self):
        record = self.table.get(self.first)
        record.json['items'] = None
        self.table.save(record)
        record = self.table.get(self.first)
        self.assertEqual(None, record.json['items'])

    def test_save_relational(self):
        record = self.relational_table.get(self.first_relational)
        record['age'] = 25
        self.relational_table.save(record)
        record = self.relational_table.get(self.first_relational)
        self.assertEqual(25, record['age'])

    def test_save_auto_commit(self):
        record = self.relational_table.get(self.first_relational)
        record['age'] = 25
        self.relational_table.save(record)
        self.relational_table.connection.rollback()
        record = self.relational_table.get(self.first_relational)
        self.assertEqual(25, record['age'])

    def test_save_without_auto_commit(self):
        record = self.relational_table.get(self.first_relational)
        record['age'] = 25
        self.relational_table.save(record, auto_commit=False)
        self.relational_table.connection.rollback()
        record = self.relational_table.get(self.first_relational)
        self.assertEqual(24, record['age'])

    def test_save_relational_with_none(self):
        record = self.relational_table.get(self.first_relational)
        record['height'] = None
        self.relational_table.save(record)
        record = self.relational_table.get(self.first_relational)
        self.assertEqual(None, record['height'])

    def test_delete_record(self):
        self.table.delete(self.first)
        record = self.table.get(self.first)
        self.assertEqual(None, record)

if __name__ == '__main__':
    unittest.main()
