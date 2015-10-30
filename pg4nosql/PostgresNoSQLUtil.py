import json
from pg4nosql.PostgresNoSQLResultItem import PostgresNoSQLResultItem
from psycopg2.extensions import adapt, AsIs

__author__ = 'cansik'


def to_sql_string(obj):
    if obj is None:
        return AsIs(obj)
    return str(obj)


def to_nullable_string(obj):
    if obj is None:
        return 'Null'
    if isinstance(obj, dict) or isinstance(obj, list):
        return adapt(json.dumps(obj))
    return adapt(str(obj))
