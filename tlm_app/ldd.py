"""
LDD telemetry handling
"""
from __future__ import annotations

from dataclasses import dataclass
from struct import unpack_from
from .ip import DATA_OFF, get_ltu_channel

LDD_PAYLOAD_FMT = "<H2xH4x4H2xH2xH"
LDD_OFF = DATA_OFF + 116
LDD_TEMP_UNIT = 0.0957
LDD_VOLT_UNIT = 108e-3

# Adjustments to temperature sensors values
RT1_ADD_DICT = {
    "LTU1.1": 1.6,
    "LTU2.1": 2.6,
    "LTU3.1": -1.5,
}

RT2_ADD_DICT = {
    "LTU1.1": 1.5,
    "LTU2.1": 2.4,
    "LTU3.1": -2.2,
}

RT3_ADD_DICT = {
    "LTU1.1": 1.5,
    "LTU2.1": 2.4,
    "LTU3.1": -3.2,
}


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
    def load_from_packet(packet: bytes) -> LddTelemetry:
        """
        Get LDD voltages and temperatures.
        """

        channel = get_ltu_channel(packet)
        ldd = unpack_from(LDD_PAYLOAD_FMT, packet, LDD_OFF)
        hv1, ldout1 = map(lambda x: LDD_VOLT_UNIT * x, ldd[0:2])
        lt1, lt2, lt3 = map(lambda x: LDD_TEMP_UNIT * x - 273, ldd[2:5])
        rt1 = LDD_TEMP_UNIT * ldd[5] - 273 + RT1_ADD_DICT[channel]
        rt2 = LDD_TEMP_UNIT * ldd[6] - 273 + RT2_ADD_DICT[channel]
        rt3 = LDD_TEMP_UNIT * ldd[7] - 273 + RT3_ADD_DICT[channel]

        return LddTelemetry(hv1, ldout1, lt1, lt2, lt3, rt1, rt2, rt3)
