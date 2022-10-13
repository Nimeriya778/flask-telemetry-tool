"""
Packets reading
"""

from typing import BinaryIO
from flask import current_app
from .models import Telemetry
from .database import db
from .channel import get_ltu_channel, is_cu_packet
from .cu import get_cutime
from .brd import BrdTelemetry
from .chg import ChgTelemetry
from .ldd import LddTelemetry
from .pls import PlsTelemetry
from .cu_unit import CUTelemetry
# from .ip import DATA_OFF


PACKET_SIZE = 1092


def get_telemetry(file: BinaryIO) -> tuple[int, set[int]]:
    """
    Get number of telemetry packets.
    """

    # pylint: disable=no-member

    count = 0
    db.session.execute(db.delete(Telemetry))
    current_app.logger.info("Deleting existing records from the database")

    ft_num = 0
    ft_lst = set()

    while packet := file.read(PACKET_SIZE):

        if is_cu_packet(packet):
            ft_num = CUTelemetry.load_from_packet(packet).ft_num
            # ft_num_tmp = CUTelemetry.load_from_packet(packet).ft_num
            # if ft_num != ft_num_tmp:
            #     ft_num = ft_num_tmp
            #     print(ft_num)
            #     print(packet[DATA_OFF + 140: DATA_OFF + 160].hex())
            continue

        try:
            channel_id = get_ltu_channel(packet)
        except KeyError:
            continue

        cutime = get_cutime(packet)

        brd = BrdTelemetry.load_from_packet(packet)
        chg = ChgTelemetry.load_from_packet(packet)
        ldd = LddTelemetry.load_from_packet(packet)
        pls = PlsTelemetry.load_from_packet(packet)

        tlm = Telemetry.from_columns(channel_id, cutime, ft_num, brd, chg, ldd, pls)
        db.session.add(tlm)
        count += 1

        ft_lst.add(ft_num)

    db.session.commit()

    return count, ft_lst
