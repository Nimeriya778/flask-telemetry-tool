"""
Control unit telemetry handling
"""

from __future__ import annotations

from dataclasses import dataclass
from struct import unpack_from
from ipaddress import IPv4Address
from .ip import DATA_OFF


CU_PAYLOAD_FMT = ">I"
CU_UNIT_OFF = DATA_OFF + 150
CU_IP = IPv4Address("255.255.255.255")


@dataclass
class CUTelemetry:
    """
    CU telemetry record
    """

    ft_num: int

    @staticmethod
    def load_from_packet(packet: bytes) -> CUTelemetry:
        """
        Get CU unit mission scenario.
        """

        cu_data = unpack_from(CU_PAYLOAD_FMT, packet, CU_UNIT_OFF)
        ft_num = cu_data[0]

        return CUTelemetry(ft_num)
