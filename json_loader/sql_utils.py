import psycopg
from constants import *


conn = psycopg.connect(f"dbname={DATABASE_NAME} user=postgres password=1234")
conn.autocommit = True


def insert_record(table_name, record):
    columns = ', '.join(record.keys())
    values = tuple(record.values())
    placeholders = ','.join(['%s'] * len(values))
    with conn.cursor() as cursor:
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        try:
            cursor.execute(sql, values)
        except psycopg.errors.UniqueViolation as e:
            print("Error: ", e)


def update_record(table_name, update_values, condition):
    set_clause = ', '.join([f"{key} = %s" for key in update_values.keys()])
    where_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])

    sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

    with conn.cursor() as cursor:
        cursor.execute(sql, list(update_values.values()) + list(condition.values()))


def get_field(table_name, field_name, conditions):
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