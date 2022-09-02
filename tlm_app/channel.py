"""
LTU channels processing
"""

from ipaddress import IPv4Address
from .models import Channel
from .database import db
from .ip import IP_OFF

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
