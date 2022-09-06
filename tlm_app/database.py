"""
Declarative mapping construction
"""

from flask_sqlalchemy import SQLAlchemy  # type: ignore
from .ip_const import LTU_IP_DICT
from .adj_const import RT_ADD_DICT


db = SQLAlchemy()


# noinspection PyArgumentList
def init_db():
    """
    Define models so that they will be registered properly on the metadata.
    """

    # pylint: disable=no-member
    # pylint: disable=import-outside-toplevel
    from tlm_app.models import Channel, Adjustment

    db.create_all()

    stmt = db.select([db.func.count()]).select_from(Channel)
    if not db.session.execute(stmt).scalar():
        for ch_ip, name in LTU_IP_DICT.items():
            channel = Channel(name=name, ip=int(ch_ip))
            db.session.add(channel)

    stmt = db.select([db.func.count()]).select_from(Adjustment)
    if not db.session.execute(stmt).scalar():
        for name, value in RT_ADD_DICT.items():
            stmt = db.select(Channel.id).where(Channel.name == name)
            result = db.session.execute(stmt)
            adj = Adjustment(
                channel_id=result.first()[0],
                ldd_rt1=value[0],
                ldd_rt2=value[1],
                ldd_rt3=value[2],
            )
            db.session.add(adj)

    db.session.commit()
