"""
Collecting data for plots
"""

from typing import List
import sqlite3
from sqlite3 import Connection, Cursor


conn = sqlite3.connect("ltu-tel.sqlite")


def retrieve_from_db(connection: Connection, columns: List[str], table: str) -> Cursor:
    """
    Create the query to get specific data
    """

    script = f"SELECT {','.join(columns)} FROM {table}"
    return connection.cursor().execute(script)


def collect_for_plot(cursor_obj: Cursor) -> List[List]:
    """
    Gather data into multiple lists
    """

    params_list: List[List] = []
    for _ in cursor_obj.description:
        params_list.append([])
    for row in cursor_obj:
        for index, elem in enumerate(row):
            params_list[index].append(elem)
    return params_list
