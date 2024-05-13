"""functions to interact with a SQL database"""


import psycopg
from .constants import *


conn = psycopg.connect(f"dbname={DATABASE_NAME} user=postgres password=1234")
conn.autocommit = True


def insert_record(table_name, record):
    """Inserts a record into a SQL table

    :param table_name: SQL table (relation) name
    :param record: a dictionary whose key-value pairs correspond to relation field-value pairs
    :return: None
    """
    columns = ', '.join(record.keys())
    values = tuple(record.values())
    placeholders = ','.join(['%s'] * len(values))
    with conn.cursor() as cursor:
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        try:
            cursor.execute(sql, values)
        except psycopg.errors.UniqueViolation as e:
            print("Error: ", e)


def update_record(table_name, update_values, conditions):
    """Updates a record in a SQL table based on a set of conditions

    :param table_name: SQL table (relation) name
    :param update_values: a dictionary whose key-value pairs correspond to relation field-value pairs to be updated
    :param conditions: a dictionary whose key-value pairs correspond to conditions for updating the records
    :return: None
    """
    set_clause = ', '.join([f"{key} = %s" for key in update_values.keys()])
    where_clause = ' AND '.join([f"{key} = %s" for key in conditions.keys()])

    sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

    with conn.cursor() as cursor:
        cursor.execute(sql, list(update_values.values()) + list(conditions.values()))


def get_field(table_name, field_name, conditions):
    """Gets a field value from a SQL table based on a set of conditions

    :param table_name: SQL table (relation) name
    :param field_name: a field whose value is to be queried from the database
    :param conditions: a dictionary whose key-value pairs correspond to conditions for updating the records
    :return: the value of the field received from the database or, if nothing is returned from the query, None
    """
    condition_keys = list(conditions.keys())
    condition_values = list(conditions.values())

    where_clause = " AND ".join(f"{key} = %s" for key in condition_keys)

    with conn.cursor() as cursor:
        sql = f"SELECT {field_name} FROM {table_name} WHERE {where_clause}"
        cursor.execute(sql, condition_values)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
