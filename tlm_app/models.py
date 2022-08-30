"""
Declaring ORM mapped classes
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from .database import Base

# pylint: disable=too-few-public-methods


class Channel(Base):
    """
    Define the mapped class for the 'channels' table.
    """

    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    channel = Column(String(10))
    ip = Column(String)


class Telemetry(Base):
    """
    Define the mapped class for the 'ltu_telemetry' table.
    """

    __tablename__ = "ltu_telemetry"

    id = Column(Integer, primary_key=True)
    chnl_id = Column(Integer, ForeignKey("channels.id"))
    cutime = Column(Integer)
    brd_lt1 = Column(Float)
    brd_lt2 = Column(Float)
    brd_lt3 = Column(Float)
    brd_lt4 = Column(Float)
    chg_vtcur1 = Column(Float)
    chg_vscur = Column(Float)
    chg_vsdiv = Column(Float)
    chg_vtdiv1 = Column(Float)
    ldd_hv1 = Column(Float)
    ldd_ldout1 = Column(Float)
    ldd_lt1 = Column(Float)
    ldd_lt2 = Column(Float)
    ldd_lt3 = Column(Float)
    ldd_rt1 = Column(Float)
    ldd_rt2 = Column(Float)
    ldd_rt3 = Column(Float)
    pls_hvr1 = Column(Float)
    pls_ldr1 = Column(Float)
    pls_ldr2 = Column(Float)
    pls_hvr2 = Column(Float)
    pls_i1 = Column(Float)
    pls_ld1 = Column(Float)
    pls_ld2 = Column(Float)
    pls_i2 = Column(Float)
    pls_i3 = Column(Float)
    pls_ld3 = Column(Float)
    pls_ld4 = Column(Float)
    pls_i4 = Column(Float)
    pls_hvf1 = Column(Float)
    pls_ldf1 = Column(Float)
    pls_ldf2 = Column(Float)
    pls_hvf2 = Column(Float)
