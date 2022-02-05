"""
PLS telemetry handling
"""
from __future__ import annotations

from dataclasses import dataclass
from struct import unpack_from
from ip import DATA_OFF

PLS_PAYLOAD_FMT = "<16H"
PLS_OFF = DATA_OFF + 144
PLS_VOLT_UNIT = 108e-3
PLS_CUR_UNIT = 31.74e-3


@dataclass
class PlsTelemetry:
    """
    PLS telemetry record
    """

    # pylint: disable=too-many-instance-attributes, invalid-name
    hvr1: float
    ldr1: float
    ldr2: float
    hvr2: float
    i1: float
    ld1: float
    ld2: float
    i2: float
    i3: float
    ld3: float
    ld4: float
    i4: float
    hvf1: float
    ldf1: float
    ldf2: float
    hvf2: float

    @staticmethod
    def load_from_packet(packet: bytes) -> PlsTelemetry:
        """
        Get PLS voltages, currents and temperatures
        """

        # pylint: disable=too-many-locals, invalid-name
        pls = unpack_from(PLS_PAYLOAD_FMT, packet, PLS_OFF)
        hvr1 = PLS_VOLT_UNIT * pls[0]
        ldr1 = PLS_VOLT_UNIT * pls[1]
        ldr2 = PLS_VOLT_UNIT * pls[2]
        hvr2 = PLS_VOLT_UNIT * pls[3]
        i1 = PLS_CUR_UNIT * pls[4]
        ld1 = PLS_VOLT_UNIT * pls[5]
        ld2 = PLS_VOLT_UNIT * pls[6]
        i2 = PLS_CUR_UNIT * pls[7]
        i3 = PLS_CUR_UNIT * pls[8]
        ld3 = PLS_VOLT_UNIT * pls[9]
        ld4 = PLS_VOLT_UNIT * pls[10]
        i4 = PLS_CUR_UNIT * pls[11]
        hvf1 = PLS_VOLT_UNIT * pls[12]
        ldf1 = PLS_VOLT_UNIT * pls[13]
        ldf2 = PLS_VOLT_UNIT * pls[14]
        hvf2 = PLS_VOLT_UNIT * pls[15]

        return PlsTelemetry(
            hvr1,
            ldr1,
            ldr2,
            hvr2,
            i1,
            ld1,
            ld2,
            i2,
            i3,
            ld3,
            ld4,
            i4,
            hvf1,
            ldf1,
            ldf2,
            hvf2,
        )
