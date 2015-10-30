from pg4nosql.PostgresNoSQLQueryStructure import PostgresNoSQLQueryStructure

__author__ = 'cansik'


class PostgresNoSQLView(PostgresNoSQLQueryStructure):
    def __init__(self, name, connection):
        super(PostgresNoSQLView, self).__init__(name, connection)
