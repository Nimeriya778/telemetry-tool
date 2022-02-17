#!/usr/bin/env python3

"""
Read telemetry and write it to database
"""

import sys
from typing import Dict, List, Tuple
from ip import get_ltu_channel
from cu import get_cutime
from brd import BrdTelemetry
from chg import ChgTelemetry
from ldd import LddTelemetry
from pls import PlsTelemetry
from db import conn, drop_table, create_table, insert_into_table

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

# Convert keys, since SQL don't allow using dots in queries
for key in tlm:
    new_key = key.replace(".", "_")
    tlm[new_key] = tlm.pop(key)

drop_table(conn, tlm)

create_table(conn, tlm)

insert_into_table(conn, tlm)

# Save the changes
conn.commit()

# Changes have been committed, so close the connection
conn.close()
