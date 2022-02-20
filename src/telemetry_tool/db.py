"""
Database handling
"""

import sqlite3
from sqlite3 import Connection
from dataclasses import astuple
from typing import Dict, List, Tuple

# Create an object that represents the database
conn = sqlite3.connect("ltu-tel.sqlite")


def drop_table(connection: Connection, data: Dict[str, List[Tuple]]) -> None:
    """
    Removes the table only if the table exists.
    Otherwise, it just ignores the statement and does nothing
    """
    # Use a dictionary key as a table name
    for key in data:
        drop_script = f"DROP TABLE IF EXISTS {key}"
        connection.cursor().execute(drop_script)


def create_table(connection: Connection, data: Dict[str, List[Tuple]]) -> None:
    """
    Creates a table to keep LTU telemetry data
    """

    for key in data:
        create_script = f"""CREATE TABLE {key}(
        id integer PRIMARY KEY,
        cutime integer, brd_lt1 real, brd_lt2 real, brd_lt3 real, brd_lt4 real,
        chg_vtcur1 real, chg_vscur real, chg_vsdiv real, chg_vtdiv1 real,
        ldd_hv1 real, ldd_ldout1 real, ldd_lt1 real, ldd_lt2 real, ldd_lt3 real,
        ldd_rt1 real, ldd_rt2 real, ldd_rt3 real, pls_hvr1 real, pls_ldr1 real,
        pls_ldr2 real, pls_hvr2 real, pls_i1 real, pls_ld1 real, pls_ld2 real,
        pls_i2 real, pls_i3 real, pls_ld3 real, pls_ld4 real, pls_i4 real,
        pls_hvf1 real, pls_ldf1 real, pls_ldf2 real, pls_hvf2 real
        )"""

        connection.cursor().execute(create_script)


def insert_into_table(connection: Connection, data: Dict[str, List[Tuple]]) -> None:
    """
    Inserts telemetry data into a table
    """

    for key, value in data.items():
        insert_script = f"""INSERT INTO {key}(
        cutime, brd_lt1, brd_lt2, brd_lt3, brd_lt4,
        chg_vtcur1, chg_vscur, chg_vsdiv, chg_vtdiv1,
        ldd_hv1, ldd_ldout1, ldd_lt1, ldd_lt2, ldd_lt3,
        ldd_rt1, ldd_rt2, ldd_rt3, pls_hvr1, pls_ldr1,
        pls_ldr2, pls_hvr2, pls_i1, pls_ld1, pls_ld2,
        pls_i2, pls_i3, pls_ld3, pls_ld4, pls_i4,
        pls_hvf1, pls_ldf1, pls_ldf2, pls_hvf2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        for row in value:
            connection.cursor().execute(
                insert_script,
                (int(row[0]),)
                + astuple(row[1])
                + astuple(row[2])
                + astuple(row[3])
                + astuple(row[4]),
            )
