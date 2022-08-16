"""
Database definition and access
"""

import sqlite3
from flask import current_app
from flask import g

# pylint: disable=invalid-name


def get_db():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """

    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
    return g.db


def close_db(err=None):
    """
    If this request connected to the database, close the connection.
    """

    # pylint: disable=unused-argument

    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    """
    Register database functions with the Flask app.
    This is called by the application factory.
    """

    app.teardown_appcontext(close_db)
