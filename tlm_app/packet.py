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


PACKET_SIZE = 1092


def get_telemetry(file: BinaryIO) -> int:
    """
    Get number of telemetry packets.
    """

    # pylint: disable=no-member

    count = 0
    db.session.execute(db.delete(Telemetry))
    current_app.logger.info("Deleting existing records from the database")

    ft_t_on = None

    while packet := file.read(PACKET_SIZE):

        if is_cu_packet(packet):
            ft_t_on = CUTelemetry.load_from_packet(packet).ft_t_on
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

        tlm = Telemetry.from_columns(channel_id, cutime, ft_t_on, brd, chg, ldd, pls)
        db.session.add(tlm)
        count += 1

    db.session.commit()

    return count
