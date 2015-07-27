from pg4nosql import DEFAULT_JSON_COLUMN_NAME


class PostgresNoSQLResultItem(object):

    def __init__(self, inner_result):
        self.__inner_result = inner_result
        self.json = self.PostgresNoSQLJSONDocument(self.__inner_result)
        self.columns = self.__inner_result.keys()

    def __str__(self):
        return str(self.__inner_result)

    def __setitem__(self, key, value):
        self.__inner_result[key] = value

    def __getitem__(self, item):
        return self.__inner_result[item]

    def get_record(self):
        return self.__inner_result

    class PostgresNoSQLJSONDocument(object):
        def __init__(self, inner_result):
            self.__inner_result = inner_result

        def __setitem__(self, key, value):
            self.__inner_result[DEFAULT_JSON_COLUMN_NAME][key] = value

        def __getitem__(self, item):
            return self.__inner_result[DEFAULT_JSON_COLUMN_NAME][item]

        def __str__(self):
            return str(self.__inner_result[DEFAULT_JSON_COLUMN_NAME])
