import psycopg2
import json
from typing import Optional, Tuple
from models import SelectResponse

with open("config.json", 'r', encoding='utf-8') as json_file:
    connection_params = json.load(json_file)


def db_select_query(sql_query: str, params: Optional[Tuple] = None) -> SelectResponse:
    with psycopg2.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_query, params)
            columns_names = [desc[0] for desc in cursor.description]
            columns = [{'title': column} for column in columns_names]
            rows = cursor.fetchall()
            data = [dict(zip(columns_names, row)) for row in rows]
            for i in range(len(data)):
                data[i]['key'] = i+1
            return SelectResponse(columns=columns, data=data)


def db_execute_query(sql_query: str, params: Optional[Tuple] = None):
    with psycopg2.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_query, params)
