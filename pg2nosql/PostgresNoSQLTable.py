import json
import psycopg2


class PostgresNoSQLTable(object):

    SQL_INSERT_JSON = "INSERT INTO %s(data) VALUES('%s') RETURNING id"
    SQL_QUERY_JSON = 'SELECT %s FROM %s WHERE %s'
    SQL_GET_JSON = 'SELECT * FROM %s WHERE id=%s'

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def put(self, data):
        self.cursor.execute(self.SQL_INSERT_JSON % (self.name, json.dumps(data)))
        return self.cursor.fetchone()[0]

    def get(self, id):
        self.cursor.execute(self.SQL_GET_JSON % (self.name, id))
        return self.cursor.fetchone()

    def query(self, query='True', columns='*'):
        self.cursor.execute(self.SQL_QUERY_JSON % (columns, self.name, query))
        rows = [item for item in self.cursor.fetchall()]
        return rows

    def drop(self):
        raise Exception('not implemented yet!')