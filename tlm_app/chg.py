"""
CHG telemetry handling
"""

from __future__ import annotations

from dataclasses import dataclass
from struct import unpack_from
from .ip import DATA_OFF


CHG_PAYLOAD_FMT = "<H2x3H"
CHG_OFF = DATA_OFF + 80
CHG_CUR_UNIT = 0.244e-3
CHG_VTDIV_UNIT = 20.1e-3
CHG_VSDIV_UNIT = 5.37e-3


@dataclass
class ChgTelemetry:
    """
    CHG telemetry record
    """

    vtcur1: float
    vscur: float
    vsdiv: float
    vtdiv1: float

    @staticmethod
    def load_from_packet(packet: bytes) -> ChgTelemetry:
        """
        Get CHG currents and voltages
        """

        chg = unpack_from(CHG_PAYLOAD_FMT, packet, CHG_OFF)
        vtcur1, vscur = map(lambda x: CHG_CUR_UNIT * x, chg[0:2])
        vsdiv = CHG_VSDIV_UNIT * chg[2]
        vtdiv1 = CHG_VTDIV_UNIT * chg[3]

        return ChgTelemetry(vtcur1, vscur, vsdiv, vtdiv1)
