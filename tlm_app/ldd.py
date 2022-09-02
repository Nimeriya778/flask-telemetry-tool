"""
LDD telemetry handling
"""

from __future__ import annotations

from dataclasses import dataclass
from struct import unpack_from
from .ip import DATA_OFF
from .database import db
from .models import Adjustment
from .channel import get_ltu_channel


LDD_PAYLOAD_FMT = "<H2xH4x4H2xH2xH"
LDD_OFF = DATA_OFF + 116
LDD_TEMP_UNIT = 0.0957
LDD_VOLT_UNIT = 108e-3


RT_ADJUSTMENTS = {}


@dataclass
class LddTelemetry:
    """
    LDD telemetry record
    """

    # pylint: disable=too-many-instance-attributes
    hv1: float
    ldout1: float
    lt1: float
    lt2: float
    lt3: float
    rt1: float
    rt2: float
    rt3: float

    @staticmethod
    def init_dct():
        """
        Initialize adjustments dictionary with the db table
        """

        # pylint: disable=no-member

        res = db.session.execute(db.select(Adjustment))
        for (rec,) in res:
            RT_ADJUSTMENTS[rec.channel_id] = rec.ldd_rt1, rec.ldd_rt2, rec.ldd_rt3

    @staticmethod
    def load_from_packet(packet: bytes) -> LddTelemetry:
        """
        Get LDD voltages and temperatures.
        """

        if not RT_ADJUSTMENTS:
            LddTelemetry.init_dct()

        channel_id = get_ltu_channel(packet)
        ldd = unpack_from(LDD_PAYLOAD_FMT, packet, LDD_OFF)
        hv1, ldout1 = map(lambda x: LDD_VOLT_UNIT * x, ldd[0:2])
        lt1, lt2, lt3 = map(lambda x: LDD_TEMP_UNIT * x - 273, ldd[2:5])
        rt1 = LDD_TEMP_UNIT * ldd[5] - 273 + RT_ADJUSTMENTS[channel_id][0]
        rt2 = LDD_TEMP_UNIT * ldd[6] - 273 + RT_ADJUSTMENTS[channel_id][1]
        rt3 = LDD_TEMP_UNIT * ldd[7] - 273 + RT_ADJUSTMENTS[channel_id][2]

        return LddTelemetry(hv1, ldout1, lt1, lt2, lt3, rt1, rt2, rt3)
