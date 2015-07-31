import os

TEST_DB_HOST = 'localhost' if 'TRAVIS' not in os.environ else os.environ['DB_HOST']
TEST_DB_USER = None if 'TRAVIS' not in os.environ else os.environ['DB_USER']
TEST_DB_PASSWORD = None if 'TRAVIS' not in os.environ else os.environ['DB_PASSWORD']

TEST_DATABASE = 'pg4nosql_test'
TEST_TABLE = 'pg4nosql_table'
TEST_RELATIONAL_TABLE = 'pg4nosql_rel_test'

TEST_TEMP_DATABASE = 'temp_db'
TEST_TEMP_TABLE = 'temp_table'

RELATIONAL_FIELDS = dict(name='text', age='integer NOT NULL', height='real')

RELATIONAL_DATA = dict(name='florian', age=24, height=179.5)
JSON_DATA = {'color': 'blue', 'items': 3}