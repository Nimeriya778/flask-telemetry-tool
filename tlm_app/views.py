"""
Application factory, configuration and URL description
"""

import os
from typing import Optional
from flask import Flask, render_template, request, abort, send_file, redirect
from werkzeug import Response
from flask.logging import create_logger
from .database import db, init_db
from .models import Channel, Telemetry
from .upload import upload_file
from .subsets import sets
from .plot import collect_for_plot, plot_telemetry


def create_app(test_config=None) -> Flask:
    """
    Create and configure an instance of the Flask application.
    """

    # pylint: disable=no-member

    app = Flask(__name__, instance_relative_config=True)
    app.logger = create_logger(app)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "ltu-tel.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create the database
    with app.app_context():
        init_db()

    @app.route("/")
    def tlm(name=None) -> str:
        return render_template("base.html", name=name)

    @app.route("/upload", methods=["GET", "POST"])
    def tlm_upload() -> str:
        return upload_file()

    @app.template_filter("fmt")
    def represent_float(float_data: float) -> str:
        return f"{float_data:.3f}"

    def collect_data(tlm_set: str, channel: Optional[str]) -> tuple[list, list]:
        stmt = db.select(Channel.id).where(Channel.name == channel)
        channel_id = db.session.execute(stmt).fetchone()[0]

        columns = [db.column(x) for x in sets[tlm_set]]
        stmt = (
            db.select(columns)
            .select_from(Telemetry)
            .where(Telemetry.channel_id == channel_id)
        )
        result = db.session.execute(stmt)
        return list(result), result.keys()

    @app.route("/table")
    def view_table() -> str:
        channel = request.args.get("channel")
        tlm_set = request.args.get("set")

        if tlm_set not in sets:
            msg = f"No such subset '{tlm_set}'"
            app.logger.error(msg)
            abort(400, msg)

        rows, columns = collect_data(tlm_set, channel)
        msg = f"Build data table for {channel} channel and {tlm_set.upper()} set"
        app.logger.info(msg)

        return render_template(
            "table.html",
            table=channel,
            rows=rows,
            columns=columns,
            set=tlm_set,
        )

    @app.route("/plot")
    def view_plot() -> str:
        channel = request.args.get("channel")
        tlm_set = request.args.get("set")

        if tlm_set not in sets:
            msg = f"No such subset '{tlm_set}'"
            app.logger.error(msg)
            abort(400, msg)

        cursor_obj, columns = collect_data(tlm_set, channel)
        params_list = collect_for_plot(cursor_obj)
        filename = f"{channel}_{tlm_set}.png"
        full_path = os.path.join(app.instance_path, "plots", filename)
        plot_telemetry(full_path, params_list, columns, channel)

        msg = f"Build data plot for {channel} channel and {tlm_set.upper()} set"
        app.logger.info(msg)

        return render_template(
            "plot.html",
            filename=filename,
        )

    @app.route("/plot/<filename>")
    def show_plot(filename: str) -> Response:
        full_path = os.path.join(app.instance_path, "plots", filename)
        return send_file(full_path, mimetype="image/png")

    @app.route("/plot/<image>")
    def open_image(filename: str) -> Response:
        full_path = os.path.join(app.instance_path, "plots", filename)
        return redirect(full_path)

    return app
