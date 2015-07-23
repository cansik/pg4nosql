import json
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor


class PostgresNoSQLTable(object):

    SQL_INSERT_JSON = "INSERT INTO %s(data %s) VALUES(%s %s) RETURNING id"
    SQL_QUERY_JSON = 'SELECT %s FROM %s WHERE %s'
    SQL_GET_JSON = 'SELECT * FROM %s WHERE id=%s'
    SQL_GET_COLUMNS = 'select column_name from information_schema.columns where table_name = %s'
    SQL_DELETE_JSON = 'DELETE FROM %s WHERE id=%s'

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.connection.cursor_factory = RealDictCursor
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def put(self, data, relational_data={}):
        # todo: replace sting concatenation with a beautiful solution
        relational_data_columns = ''
        relational_data_values = ''

        if relational_data:
            relational_data_columns = ',' + ",".join(relational_data.keys())
            relational_data_values = ",'" + "','".join(relational_data.values()) + "'"

        self.cursor.execute(self.SQL_INSERT_JSON, (AsIs(self.name), AsIs(relational_data_columns), json.dumps(data), AsIs(relational_data_values)))
        return self.cursor.fetchone()['id']

    def get_document(self, object_id):
        return self.get(object_id)['data']

    def get(self, object_id):
        self.cursor.execute(self.SQL_GET_JSON, (AsIs(self.name), object_id))
        return self.cursor.fetchone()

    def query(self, query='True', columns='*'):
        self.cursor.execute(self.SQL_QUERY_JSON, (AsIs(columns), AsIs(self.name), AsIs(query)))
        rows = [item for item in self.cursor.fetchall()]
        return rows

    def get_columns(self):
        self.cursor.execute(self.SQL_GET_COLUMNS, (self.name,))
        columns = map(lambda m: m['column_name'], self.cursor.fetchall())
        return columns

    def delete(self, object_id):
        self.cursor.execute(self.SQL_DELETE_JSON, (AsIs(self.name), object_id))
