"""
Control unit telemetry handling
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from struct import unpack_from
from ipaddress import IPv4Address
from .ip import DATA_OFF
from .timestamp import ton_to_unixtime


CU_PAYLOAD_FMT = "<I"
CU_UNIT_OFF = DATA_OFF + 150
CU_IP = IPv4Address("255.255.255.255")
T_ON_OFF = 8


@dataclass
class CUTelemetry:
    """
    CU telemetry record
    """

    ft_t_on: datetime

    @staticmethod
    def load_from_packet(packet: bytes) -> CUTelemetry:
        """
        Get CU unit mission scenario.
        """

        (t_on,) = unpack_from(CU_PAYLOAD_FMT, packet, CU_UNIT_OFF + T_ON_OFF)

        ft_t_on = ton_to_unixtime(t_on)

        return CUTelemetry(ft_t_on)
