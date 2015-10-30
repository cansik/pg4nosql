from pg4nosql import DEFAULT_JSON_COLUMN_NAME, DEFAULT_ROW_IDENTIFIER


class PostgresNoSQLResultItem(object):

    def __init__(self, inner_result, origin_table):
        self.__inner_result = inner_result
        self.json = self.PostgresNoSQLJSONDocument(self.__inner_result)
        self.columns = self.__inner_result.keys()
        self.id = self.__inner_result.get(DEFAULT_ROW_IDENTIFIER, None)
        self.__origin_table = origin_table

    def __str__(self):
        return str(self.__inner_result)

    def __setitem__(self, key, value):
        self.__inner_result[key] = value

    def __getitem__(self, item):
        return self.__inner_result[item]

    def get_record(self):
        return self.__inner_result

    def save(self, auto_commit=True):
        if DEFAULT_ROW_IDENTIFIER not in self.columns:
            raise NotImplementedError('ResultItem does not contain column "%s"!' % DEFAULT_ROW_IDENTIFIER)
        self.__origin_table.save(self, auto_commit=auto_commit)

    class PostgresNoSQLJSONDocument(object):
        def __init__(self, inner_result):
            self.__inner_result = inner_result

        def __setitem__(self, key, value):
            self.__inner_result[DEFAULT_JSON_COLUMN_NAME][key] = value

        def __getitem__(self, item):
            return self.__inner_result[DEFAULT_JSON_COLUMN_NAME][item]

        def __str__(self):
            return str(self.__inner_result[DEFAULT_JSON_COLUMN_NAME])
