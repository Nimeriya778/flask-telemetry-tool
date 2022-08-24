"""
IP handling
"""

from ipaddress import IPv4Address

# All parameters sizes are in bytes
MAC_HEADER = 14
IPV4_HEADER = 20
IP_SADDR = 4
IP_DADDR = 4
UDP_HEADER = 8
SEQ_ID = 4

# To find out where source IP address is started, calculate its start position
IP_OFF = MAC_HEADER + IPV4_HEADER - IP_SADDR - IP_DADDR

# To find out where DATA is started, calculate its start position
DATA_OFF = MAC_HEADER + IPV4_HEADER + UDP_HEADER + SEQ_ID

LTU_IP_DICT = {
    IPv4Address("172.16.1.11"): "LTU1.1",
    IPv4Address("172.16.1.21"): "LTU2.1",
    IPv4Address("172.16.1.31"): "LTU3.1",
    IPv4Address("172.16.1.12"): "LTU1.2",
    IPv4Address("172.16.1.22"): "LTU2.2",
    IPv4Address("172.16.1.32"): "LTU3.2",
}


def get_ltu_channel(packet: bytes) -> str:
    """
    Returns the LTU channel from LTU IP address
    """

    ip_saddr = IPv4Address(packet[IP_OFF: IP_OFF + 4])
    return LTU_IP_DICT[ip_saddr]
