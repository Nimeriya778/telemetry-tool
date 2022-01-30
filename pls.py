"""
PLS telemetry handling
"""

from dataclasses import dataclass


@dataclass
class PlsTelemetry:
    """
    PLS telemetry record
    """

    # pylint: disable=too-many-instance-attributes
    pls_hvr1: float
    pls_ldr1: float
    pls_ldr2: float
    pls_hvr2: float
    pls_i1: float
    pls_ld1: float
    pls_ld2: float
    pls_i2: float
    pls_i3: float
    pls_ld3: float
    pls_ld4: float
    pls_i4: float
    pls_hvf1: float
    pls_ldf1: float
    pls_ldf2: float
    pls_hvf2: float
