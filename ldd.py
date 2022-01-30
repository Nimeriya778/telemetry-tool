"""
LDD telemetry handling
"""

from dataclasses import dataclass


@dataclass
class LddTelemetry:
    """
    LDD telemetry record
    """

    # pylint: disable=too-many-instance-attributes
    ldd_hv1: float
    ldd_ldout1: float
    ldd_lt1: float
    ldd_lt2: float
    ldd_lt3: float
    ldd_rt1: float
    ldd_rt2: float
    ldd_rt3: float
