"""
Packets reading
"""

from typing import BinaryIO, Dict, List, Tuple
from .ip import get_ltu_channel
from .cu import get_cutime
from .brd import BrdTelemetry
from .chg import ChgTelemetry
from .ldd import LddTelemetry
from .pls import PlsTelemetry

PACKET_SIZE = 1092


def get_telemetry(file: BinaryIO) -> Dict[str, List[Tuple]]:
    """
    Gets telemetry data from packets
    """

    tlm: Dict[str, List[Tuple]] = {"LTU1.1": [], "LTU2.1": [], "LTU3.1": []}

    while packet := file.read(PACKET_SIZE):

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
        # Convert keys, since SQL don't allow using dots in queries
    for key in tlm:
        new_key = key.replace(".", "_")
        tlm[new_key] = tlm.pop(key)

    return tlm
