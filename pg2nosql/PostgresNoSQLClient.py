import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor
from PostgresNoSQLTable import PostgresNoSQLTable


class PostgresNoSQLClient(object):
    SQL_CREATE_JSON_TABLE = 'CREATE TABLE %s (id SERIAL %s, data JSON);'
    SQL_DROP_JSON_TABLE = 'DROP TABLE IF EXISTS %s;'
    SQL_TABLE_EXISTS = "SELECT EXISTS(SELECT relname FROM pg_class WHERE relname=%s)"

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, host, database, user=None, password=None):
        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.cursor = self.connection.cursor()

    def close(self):
        return self.connection.close()

    def create_table(self, table_name, relational_columns={}):
        # create additional columns string
        columns_str = ''.join(', %s %s' % (key, val) for (key, val) in relational_columns.iteritems())
        self.cursor.execute(self.SQL_CREATE_JSON_TABLE, (AsIs(table_name), AsIs(columns_str)))
        self.commit()
        return PostgresNoSQLTable(table_name, self.connection)

    def drop_table(self, table_name):
        self.cursor.execute(self.SQL_DROP_JSON_TABLE, (AsIs(table_name),))
        self.commit()

    def get_table(self, table_name):
        if self.table_exists(table_name):
            return PostgresNoSQLTable(table_name, self.connection)
        else:
            return None

    def commit(self):
        self.connection.commit()

    def table_exists(self, table_name):
        exists = False
        try:
            self.cursor.execute(self.SQL_TABLE_EXISTS, (table_name,))
            exists = self.cursor.fetchone()[0]
        except psycopg2.Error as e:
            print e
        return exists
