"""
PLS telemetry handling
"""
from __future__ import annotations

from dataclasses import dataclass
from struct import unpack_from
from .ip import DATA_OFF

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
        hvr1, ldr1, ldr2, hvr2, hvf1, ldf1, ldf2, hvf2, ld1, ld2, ld3, ld4 = map(
            lambda x: PLS_VOLT_UNIT * x, pls[0:4] + pls[12:16] + pls[5:7] + pls[9:11]
        )
        i1, i4, i2, i3 = map(lambda x: PLS_CUR_UNIT * x, pls[4:12:7] + pls[7:9])

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
