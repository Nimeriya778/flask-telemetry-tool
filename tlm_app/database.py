"""
Declarative mapping construction
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

engine = create_engine("sqlite://")
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    """
    Construct a base class for declarative class definitions.
    The class is defined explicitly to support the Mypy plugin.
    """

    # pylint: disable=too-few-public-methods

    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


def init_db():
    """
    Define models so that they will be registered properly on the metadata.
    """

    import tlm_app.models

    Base.metadata.create_all(bind=engine)
