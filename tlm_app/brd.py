"""
BRD telemetry handling
"""

from __future__ import annotations

from dataclasses import dataclass
from struct import unpack_from
from .ip import DATA_OFF

BRD_PAYLOAD_FMT = "<4H"
BRD_OFF = DATA_OFF + 72
BRD_TEMP_UNIT = 0.488


@dataclass
class BrdTelemetry:
    """
    BRD telemetry record
    """

    lt1: float
    lt2: float
    lt3: float
    lt4: float

    @staticmethod
    def load_from_packet(packet: bytes) -> BrdTelemetry:
        """
        Get BRD temperatures.
        """

        temps = unpack_from(BRD_PAYLOAD_FMT, packet, BRD_OFF)
        lt1, lt2, lt3, lt4 = map(lambda x: BRD_TEMP_UNIT * x - 273, temps)

        return BrdTelemetry(lt1, lt2, lt3, lt4)
