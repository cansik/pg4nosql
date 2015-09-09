import copy
import json
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor
from pg4nosql import DEFAULT_JSON_COLUMN_NAME, DEFAULT_ROW_IDENTIFIER
from pg4nosql.PostgresNoSQLResultItem import PostgresNoSQLResultItem
from psycopg2.extensions import adapt


class PostgresNoSQLTable(object):
    __SQL_INSERT_JSON = "INSERT INTO %s(" + DEFAULT_JSON_COLUMN_NAME + " %s) VALUES(%s %s) RETURNING " + DEFAULT_ROW_IDENTIFIER
    __SQL_QUERY_JSON = 'SELECT %s FROM %s WHERE %s'
    __SQL_GET_JSON = 'SELECT * FROM %s WHERE ' + DEFAULT_ROW_IDENTIFIER + '=%s'
    __SQL_GET_COLUMNS = 'select column_name from information_schema.columns where table_name = %s'
    __SQL_DELETE_JSON = 'DELETE FROM %s WHERE ' + DEFAULT_ROW_IDENTIFIER + '=%s'
    __SQL_UPDATE_JSON = 'UPDATE %s SET ' + DEFAULT_JSON_COLUMN_NAME + '=%s %s WHERE ' + DEFAULT_ROW_IDENTIFIER + '=%s;'

    __SQL_INSERT = "INSERT INTO %s(%s) VALUES(%s) RETURNING " + DEFAULT_ROW_IDENTIFIER
    __SQL_UPDATE = 'UPDATE %s SET %s WHERE ' + DEFAULT_ROW_IDENTIFIER + '=%s;'

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.connection.cursor_factory = RealDictCursor
        self.cursor = self.connection.cursor()

    @staticmethod
    def __to_sql_string(obj):
        if obj is None:
            return AsIs(obj)
        return str(obj)

    @staticmethod
    def __to_nullable_string(obj):
        if obj is None:
            return 'Null'
        if isinstance(obj, dict) or isinstance(obj, list):
            return adapt(json.dumps(obj))
        return adapt(str(obj))

    def commit(self):
        """
        Use commit only if auto_commit in put or save are disabled!
        :return: None
        """
        self.connection.commit()

    def insert(self, auto_commit=True, **data):
        # filter none values out
        relational_data = {k: v for (k, v) in data.items() if v is not None}

        relational_data_columns = ''
        relational_data_values = ''

        if relational_data:
            relational_data_columns = ",".join(relational_data.keys())
            relational_data_values = "'" + "','".join(map(str, relational_data.values())) + "'"

        self.cursor.execute(self.__SQL_INSERT, (AsIs(self.name),
                                                AsIs(relational_data_columns),
                                                AsIs(relational_data_values)))

        if auto_commit:
            self.commit()

        return self.cursor.fetchone()[DEFAULT_ROW_IDENTIFIER]

    def update(self, record, auto_commit=True):
        record = copy.deepcopy(record.get_record())

        object_id = record.pop(DEFAULT_ROW_IDENTIFIER)

        relational_data_sql = ','.join(
            "%s=%s" % (key, str(self.__to_nullable_string(val))) for (key, val) in record.items())

        self.cursor.execute(self.__SQL_UPDATE, (AsIs(self.name),
                                                AsIs(relational_data_sql), object_id))

        if auto_commit:
            self.commit()

    def put(self, json_data, auto_commit=True, **relational_data):
        # filter none values out
        relational_data = {k: v for (k, v) in relational_data.items() if v is not None}

        # todo: replace string concatenation with a beautiful solution
        relational_data_columns = ''
        relational_data_values = ''

        if relational_data:
            relational_data_columns = ',' + ",".join(relational_data.keys())
            relational_data_values = ",'" + "','".join(map(str, relational_data.values())) + "'"

        self.cursor.execute(self.__SQL_INSERT_JSON, (AsIs(self.name),
                                                     AsIs(relational_data_columns), json.dumps(json_data),
                                                     AsIs(relational_data_values)))
        if auto_commit:
            self.commit()

        return self.cursor.fetchone()[DEFAULT_ROW_IDENTIFIER]

    def save(self, record, auto_commit=True):
        record = copy.deepcopy(record.get_record())

        data = record.pop(DEFAULT_JSON_COLUMN_NAME)
        object_id = record.pop(DEFAULT_ROW_IDENTIFIER)

        relational_data_sql = ''.join(
            ", %s=%s" % (key, self.__to_nullable_string(val)) for (key, val) in record.items())

        self.cursor.execute(self.__SQL_UPDATE_JSON, (AsIs(self.name),
                                                     json.dumps(data), AsIs(relational_data_sql), object_id))

        if auto_commit:
            self.commit()

    def get(self, object_id):
        self.cursor.execute(self.__SQL_GET_JSON, (AsIs(self.name), object_id))
        record = self.cursor.fetchone()

        if record is None:
            return record

        return PostgresNoSQLResultItem(record)

    def query(self, query='True', columns='*'):
        self.cursor.execute(self.__SQL_QUERY_JSON, (AsIs(columns), AsIs(self.name), AsIs(query)))
        rows = [item for item in self.cursor.fetchall()]
        items = map(lambda r: PostgresNoSQLResultItem(r), rows)
        return items

    def query_one(self, query='True', columns='*'):
        result = self.query(query, columns)
        if not result:
            return None
        return result[0]

    def get_columns(self):
        self.cursor.execute(self.__SQL_GET_COLUMNS, (self.name,))
        columns = map(lambda m: m['column_name'], self.cursor.fetchall())
        return columns

    def delete(self, object_id, auto_commit=True):
        self.cursor.execute(self.__SQL_DELETE_JSON, (AsIs(self.name), object_id))
        if auto_commit:
            self.commit()

    def execute(self, sql_query):
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()
