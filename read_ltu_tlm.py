#!/usr/bin/env python3

"""
Read telemetry and write it to database
"""

from dataclasses import astuple
import sys
import sqlite3
from typing import Dict, List, Tuple
from ip import get_ltu_channel
from cu import get_cutime
from brd import BrdTelemetry
from chg import ChgTelemetry
from ldd import LddTelemetry
from pls import PlsTelemetry

# sys.argv is a list, which contains the command-line arguments passed to the script.
# The first item of this list contains the name of the script itself.
filename = sys.argv[1]

tlm: Dict[str, List[Tuple]] = {"LTU1.1": [], "LTU2.1": [], "LTU3.1": []}

PACKET_COUNT = 0
with open(filename, "rb") as binary_file:

    while packet := binary_file.read(1092):
        PACKET_COUNT += 1

        try:
            channel = get_ltu_channel(packet)
        except KeyError:
            continue

        cutime = get_cutime(packet)
        brd = BrdTelemetry.load_from_packet(packet)
        chg = ChgTelemetry.load_from_packet(packet)
        ldd = LddTelemetry.load_from_packet(packet)
        pls = PlsTelemetry.load_from_packet(packet)

        tlm[channel].append((cutime, brd, chg, ldd, pls))
    print(f"Total number of packets is {PACKET_COUNT}")

# To use sqlite3 module create an object that represents the database.
conn = sqlite3.connect("ltu-tel.sqlite")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS telemetry_ltu11")

# Create table
cur.execute(
    """CREATE TABLE telemetry_ltu11(
        id integer PRIMARY KEY,
        /* cutime is timestamp, \
        since there is no timestamp datatype in sqlite,\
        define as integer datatype (UNIX time). */
        cutime integer,
        brd_lt1 real, brd_lt2 real, brd_lt3 real, brd_lt4 real,
        chg_vtcur1 real, chg_vscur real, chg_vsdiv real, chg_vtdiv1 real,
        ldd_hv1 real, ldd_ldout1 real, ldd_lt1 real, ldd_lt2 real, ldd_lt3 real,
        ldd_rt1 real, ldd_rt2 real, ldd_rt3 real, pls_hvr1 real, pls_ldr1 real,
        pls_ldr2 real, pls_hvr2 real, pls_i1 real, pls_ld1 real, pls_ld2 real,
        pls_i2 real, pls_i3 real, pls_ld3 real, pls_ld4 real, pls_i4 real,
        pls_hvf1 real, pls_ldf1 real, pls_ldf2 real, pls_hvf2 real)
        """
)

for row in tlm["LTU1.1"]:
    cur.execute(
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
