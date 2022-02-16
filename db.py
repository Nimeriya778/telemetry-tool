"""
Database handling
"""

import sqlite3
from sqlite3 import Connection, Cursor
from dataclasses import astuple

# Create an object that represents the database
conn = sqlite3.connect("ltu-tel.sqlite")

tlm = {"LTU1_1": [], "LTU2_1": [], "LTU3_1": []}


def drop_table(dict_key_name: str) -> Cursor:
    """
    Removes the table only if the table exists.
    Otherwise, it just ignores the statement and does nothing
    """

    for table in dict_key_name:
        drop_script = f"DROP TABLE IF EXISTS {table}"
        return conn.cursor().execute(drop_script)


def create_table(connection: Connection, table_name: str) -> Cursor:
    """
    Creates a table to keep LTU telemetry data
    """

    create_script = f"""CREATE TABLE {table_name}(
    id integer PRIMARY KEY,
    cutime integer, brd_lt1 real, brd_lt2 real, brd_lt3 real, brd_lt4 real,
    chg_vtcur1 real, chg_vscur real, chg_vsdiv real, chg_vtdiv1 real,
    ldd_hv1 real, ldd_ldout1 real, ldd_lt1 real, ldd_lt2 real, ldd_lt3 real,
    ldd_rt1 real, ldd_rt2 real, ldd_rt3 real, pls_hvr1 real, pls_ldr1 real,
    pls_ldr2 real, pls_hvr2 real, pls_i1 real, pls_ld1 real, pls_ld2 real,
    pls_i2 real, pls_i3 real, pls_ld3 real, pls_ld4 real, pls_i4 real,
    pls_hvf1 real, pls_ldf1 real, pls_ldf2 real, pls_hvf2 real
    )"""

    return connection.cursor().execute(create_script)


def insert_into_table(cursor_obj: Cursor) -> Cursor:
    """
    Inserts telemetry data into a table
    """

    for row in cursor_obj:
        cursor_obj.execute(
            """INSERT INTO telemetry_ltu11(
            cutime, brd_lt1, brd_lt2, brd_lt3, brd_lt4,
            chg_vtcur1, chg_vscur, chg_vsdiv, chg_vtdiv1,
            ldd_hv1, ldd_ldout1, ldd_lt1, ldd_lt2, ldd_lt3,
            ldd_rt1, ldd_rt2, ldd_rt3, pls_hvr1, pls_ldr1,
            pls_ldr2, pls_hvr2, pls_i1, pls_ld1, pls_ld2,
            pls_i2, pls_i3, pls_ld3, pls_ld4, pls_i4,
            pls_hvf1, pls_ldf1, pls_ldf2, pls_hvf2)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (int(row[0]),)
            + astuple(row[1])
            + astuple(row[2])
            + astuple(row[3])
            + astuple(row[4]),
        )


# Save (commit) the changes
conn.commit()

# Changes have been committed, so close the connection
conn.close()
