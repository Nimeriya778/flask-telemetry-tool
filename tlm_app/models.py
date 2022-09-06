"""
Declaring ORM mapped classes
"""

from typing import TypeAlias
from datetime import datetime
from flask_sqlalchemy.model import DefaultMeta  # type: ignore
from .database import db


BaseModel: DefaultMeta = db.Model

# pylint: disable=too-few-public-methods
# pylint: disable=no-member


class Channel(BaseModel):
    """
    Define the mapped class for the 'channels' table.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    ip = db.Column(db.Integer, unique=True)


class Adjustment(BaseModel):
    """
    Define the mapped class for the 'adjustments' table.
    """

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"))
    ldd_rt1 = db.Column(db.Float)
    ldd_rt2 = db.Column(db.Float)
    ldd_rt3 = db.Column(db.Float)


# noinspection PyArgumentList
class Telemetry(BaseModel):
    """
    Define the mapped class for the 'ltu_telemetry' table.
    """

    # pylint: disable=too-many-arguments

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"))
    cutime = db.Column(db.DateTime)
    brd_lt1 = db.Column(db.Float)
    brd_lt2 = db.Column(db.Float)
    brd_lt3 = db.Column(db.Float)
    brd_lt4 = db.Column(db.Float)
    chg_vtcur1 = db.Column(db.Float)
    chg_vscur = db.Column(db.Float)
    chg_vsdiv = db.Column(db.Float)
    chg_vtdiv1 = db.Column(db.Float)
    ldd_hv1 = db.Column(db.Float)
    ldd_ldout1 = db.Column(db.Float)
    ldd_lt1 = db.Column(db.Float)
    ldd_lt2 = db.Column(db.Float)
    ldd_lt3 = db.Column(db.Float)
    ldd_rt1 = db.Column(db.Float)
    ldd_rt2 = db.Column(db.Float)
    ldd_rt3 = db.Column(db.Float)
    pls_hvr1 = db.Column(db.Float)
    pls_ldr1 = db.Column(db.Float)
    pls_ldr2 = db.Column(db.Float)
    pls_hvr2 = db.Column(db.Float)
    pls_i1 = db.Column(db.Float)
    pls_ld1 = db.Column(db.Float)
    pls_ld2 = db.Column(db.Float)
    pls_i2 = db.Column(db.Float)
    pls_i3 = db.Column(db.Float)
    pls_ld3 = db.Column(db.Float)
    pls_ld4 = db.Column(db.Float)
    pls_i4 = db.Column(db.Float)
    pls_hvf1 = db.Column(db.Float)
    pls_ldf1 = db.Column(db.Float)
    pls_ldf2 = db.Column(db.Float)
    pls_hvf2 = db.Column(db.Float)

    @staticmethod
    def from_columns(
        channel_id,
        cutm: datetime,
        brd: TypeAlias = "BrdTelemetry",
        chg: TypeAlias = "ChgTelemetry",
        ldd: TypeAlias = "LddTelemetry",
        pls: TypeAlias = "PlsTelemetry",
    ):
        """
        Unite columns from telemetry file to fill the table.
        """

        return Telemetry(
            channel_id=channel_id,
            cutime=cutm,
            brd_lt1=brd.lt1,
            brd_lt2=brd.lt2,
            brd_lt3=brd.lt3,
            brd_lt4=brd.lt4,
            chg_vtcur1=chg.vtcur1,
            chg_vscur=chg.vscur,
            chg_vsdiv=chg.vsdiv,
            chg_vtdiv1=chg.vtdiv1,
            ldd_hv1=ldd.hv1,
            ldd_ldout1=ldd.ldout1,
            ldd_lt1=ldd.lt1,
            ldd_lt2=ldd.lt2,
            ldd_lt3=ldd.lt3,
            ldd_rt1=ldd.rt1,
            ldd_rt2=ldd.rt2,
            ldd_rt3=ldd.rt3,
            pls_hvr1=pls.hvr1,
            pls_ldr1=pls.ldr1,
            pls_ldr2=pls.ldr2,
            pls_hvr2=pls.hvr2,
            pls_i1=pls.i1,
            pls_ld1=pls.ld1,
            pls_ld2=pls.ld2,
            pls_i2=pls.i2,
            pls_i3=pls.i3,
            pls_ld3=pls.ld3,
            pls_ld4=pls.ld4,
            pls_i4=pls.i4,
            pls_hvf1=pls.hvf1,
            pls_ldf1=pls.ldf1,
            pls_ldf2=pls.ldf2,
            pls_hvf2=pls.hvf2,
        )
