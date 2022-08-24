"""
Packets reading
"""

from typing import BinaryIO
from .ip import get_ltu_channel
from .cu import get_cutime
from .brd import BrdTelemetry
from .chg import ChgTelemetry
from .ldd import LddTelemetry
from .pls import PlsTelemetry

PACKET_SIZE = 1092


def get_telemetry(file: BinaryIO) -> dict[str, list[tuple]]:
    """
    Gets telemetry data from packets
    """

    tlm: dict[str, list[tuple]] = {"LTU1.1": [], "LTU2.1": [], "LTU3.1": []}

    while packet := file.read(PACKET_SIZE):

        try:
            channel = get_ltu_channel(packet)
        except KeyError:
            continue

        cutime = get_cutime(packet)
        brd = BrdTelemetry.load_from_packet(packet)
        chg = ChgTelemetry.load_from_packet(packet)
        ldd = LddTelemetry.load_from_packet(packet)
        pls = PlsTelemetry.load_from_packet(packet)

        tlm[channel].append((cutime, brd, chg, ldd, pls))

        # Convert keys, since SQL doesn't allow using dots in queries
        for key in tlm:
            new_key = key.replace(".", "_")
            tlm[new_key] = tlm.pop(key)

    return tlm
