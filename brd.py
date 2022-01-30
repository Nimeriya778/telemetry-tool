"""
BRD telemetry handling
"""

from dataclasses import dataclass


@dataclass
class BrdTelemetry:
    """
    BRD telemetry record
    """

    brd_lt1: float
    brd_lt2: float
    brd_lt3: float
    brd_lt4: float
