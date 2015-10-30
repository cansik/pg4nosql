
from psycopg2.extras import RealDictCursor
from pg4nosql.PostgresNoSQLResultItem import PostgresNoSQLResultItem
from psycopg2.extensions import AsIs

__author__ = 'cansik'


class PostgresNoSQLQueryStructure(object):
    __SQL_QUERY_JSON = 'SELECT %s FROM %s WHERE %s'

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.connection.cursor_factory = RealDictCursor
        self.cursor = self.connection.cursor()

    def query(self, query='True', columns='*'):
        self.cursor.execute(self.__SQL_QUERY_JSON,
                            (AsIs(columns), AsIs(self.name), AsIs(query)))
        rows = [item for item in self.cursor.fetchall()]
        items = map(lambda r: PostgresNoSQLResultItem(r, self), rows)
        return list(items)
