import psycopg2
from psycopg2.extensions import AsIs
from pg4nosql import DEFAULT_POSTGRES_DATABASE, DEFAULT_POSTGRES_PORT
from pg4nosql.PostgresNoSQLDatabase import PostgresNoSQLDatabase


class PostgresNoSQLClient(object):
    """
    Creates new connections and
    """

    __SQL_DATABASE_EXISTS = 'SELECT EXISTS(SELECT datname FROM pg_database WHERE datname=%s)'
    __SQL_CREATE_DATABASE = 'CREATE DATABASE %s'
    __SQL_DROP_DATABASE = 'DROP DATABASE IF EXISTS %s'

    def __init__(self, host, database=DEFAULT_POSTGRES_DATABASE, port=DEFAULT_POSTGRES_PORT, user=None, password=None):
        # public fields
        self.host = host
        self.database = database
        self.port = port

        # private
        self.__user = user
        self.__password = password
        self.__connection = None
        self.__cursor = None

        # helps to make multiple functions with one connection
        self.__connect_counter = 0

    def __commit(self):
        self.__connection.commit()

    def __connect(self):
        self.__connect_counter += 1
        if not self.__connection:
            self.__connection = psycopg2.connect(host=self.host, database=self.database, port=self.port,
                                                 user=self.__user, password=self.__password)
            self.__connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.__cursor = self.__connection.cursor()

    def __close(self):
        self.__connect_counter -= 1

        if self.__connect_counter is 0:
            self.__connection.close()
            self.__connection = None

        return self.__connect_counter is 0

    def __create_db_object(self, database_name):
        return PostgresNoSQLDatabase(name=database_name, host=self.host, port=self.port, user=self.__user,
                                     password=self.__password)

    def get_database(self, database_name):
        self.__connect()
        db_object = None

        if self.database_exists(database_name):
            db_object = self.__create_db_object(database_name)

        self.__close()
        return db_object

    def get_or_create_database(self, database_name):
        self.__connect()
        db = self.get_database(database_name)
        if not db:
            db = self.create_database(database_name)
        self.__close()
        return db

    def create_database(self, database_name):
        self.__connect()
        self.__cursor.execute(self.__SQL_CREATE_DATABASE, (AsIs(database_name),))
        self.__commit()
        self.__close()
        return self.__create_db_object(database_name)

    def drop_database(self, database_name):
        self.__connect()
        self.__cursor.execute(self.__SQL_DROP_DATABASE, (AsIs(database_name),))
        self.__close()

    def database_exists(self, database_name):
        self.__connect()
        exists = False
        try:
            self.__cursor.execute(self.__SQL_DATABASE_EXISTS, (database_name,))
            exists = self.__cursor.fetchone()[0]
        except psycopg2.Error as e:
            print e
        self.__close()
        return exists

    def __getitem__(self, item):
        return self.get_or_create_database(item)
