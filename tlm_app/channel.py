"""
LTU channels processing
"""

from ipaddress import IPv4Address
from struct import unpack_from
from .models import Channel
from .database import db
from .ip import IP_OFF, DATA_OFF
from .cu_unit import CU_IP

CHANNELS = {}


def init_dct():
    """
    Initialize channels dictionary with the db table
    """

    # pylint: disable=no-member

    res = db.session.execute(db.select(Channel.ip, Channel.id))
    for ch_ip, ch_id in res:
        CHANNELS[ch_ip] = ch_id


def get_ltu_channel(packet: bytes) -> int:
    """
    Return the LTU channel id from LTU IP address.
    """

    if not CHANNELS:
        init_dct()

    ch_ip = int(IPv4Address(packet[IP_OFF: IP_OFF + 4]))

    return CHANNELS[ch_ip]


def is_cu_packet(packet: bytes) -> bool:
    """
    Check if the packet is a CU packet
    """

    ch_ip = IPv4Address(packet[IP_OFF: IP_OFF + 4])
    sub_type = unpack_from("<H", packet, DATA_OFF + 8)

    return ch_ip == CU_IP and sub_type[0] == 1
