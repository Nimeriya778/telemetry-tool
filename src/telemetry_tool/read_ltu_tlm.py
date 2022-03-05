#!/usr/bin/env python3

"""
Read telemetry and write it to database
"""

import sys
from .packet import get_telemetry
from .db import conn, drop_table, create_table, insert_into_table

# sys.argv is a list, which contains the command-line arguments passed to the script.
# The first item of this list contains the name of the script itself.
filename = sys.argv[1]

with open(filename, "rb") as file:
    tlm = get_telemetry(file)

drop_table(conn, tlm)

create_table(conn, tlm)

insert_into_table(conn, tlm)

conn.commit()
conn.close()
