"""
CUTIME telemetry handling
"""

from datetime import datetime
from .ip import DATA_OFF
from .timestamp import timestamp_to_unixtime

CUTIME_OFF = DATA_OFF + 44
CUTIME_W = 8


def get_cutime(packet: bytes) -> datetime:
    """
    Get CU time in the Unix time format.
    """

    tstamp = int.from_bytes(
        packet[CUTIME_OFF: CUTIME_OFF + CUTIME_W], byteorder="little"
    )

    return timestamp_to_unixtime(tstamp)
