"""
LTU Ips grouping to record in the database
"""

from ipaddress import IPv4Address

LTU_IP_DICT = {
    IPv4Address("172.16.1.11"): "LTU1.1",
    IPv4Address("172.16.1.21"): "LTU2.1",
    IPv4Address("172.16.1.31"): "LTU3.1",
    IPv4Address("172.16.1.12"): "LTU1.2",
    IPv4Address("172.16.1.22"): "LTU2.2",
    IPv4Address("172.16.1.32"): "LTU3.2",
}
