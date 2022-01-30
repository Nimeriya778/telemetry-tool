"""
CHG telemetry handling
"""

from dataclasses import dataclass


@dataclass
class ChgTelemetry:
    """
    CHG telemetry record
    """

    chg_vtcur1: float
    chg_vtdiv1: float
    chg_vscur: float
    chg_vsdiv: float
