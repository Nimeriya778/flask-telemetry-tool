"""
Offset calculations
"""

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
