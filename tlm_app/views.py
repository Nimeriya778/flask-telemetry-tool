"""
Application factory, configuration and URL description
"""

import os
from flask import Flask, render_template, request, abort, send_file, redirect
from flask.logging import create_logger
from werkzeug import Response
from .database import db, init_db
from .upload import upload_file
from .subsets import sets
from .plot import collect_data, collect_for_plot, plot_telemetry


def create_app(test_config=None) -> Flask:
    """
    Create and configure an instance of the Flask application.
    """

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
        app.logger.info("Uploading the file")
        return upload_file()

    @app.template_filter("fmt")
    def represent_float(float_data: float) -> str:
        return f"{float_data:.3f}"

    def validate_request() -> tuple[str, str]:
        channel = request.args.get("channel")
        tlm_set = request.args.get("set")

        if channel is None or tlm_set is None:
            msg = "Missing arguments"
            raise ValueError(msg)

        if tlm_set not in sets:
            msg = f"No such subset '{tlm_set}'"
            raise ValueError(msg)

        return tlm_set, channel

    # pylint: disable=logging-fstring-interpolation

    @app.route("/table")
    def view_table() -> str:
        try:
            tlm_set, channel = validate_request()
        except ValueError as err:
            app.logger.error(str(err))
            abort(400, str(err))

        # noinspection PyUnboundLocalVariable
        rows, columns = collect_data(tlm_set, channel)
        app.logger.debug(f"Collected {len(rows)} rows, {len(columns)} columns")
        app.logger.info(
            f"Building data table for {channel} channel and {tlm_set.upper()} set"
        )

        return render_template(
            "table.html",
            table=channel,
            rows=rows,
            columns=columns,
            set=tlm_set,
        )

    @app.route("/plot")
    def view_plot() -> str:
        try:
            tlm_set, channel = validate_request()
        except ValueError as err:
            app.logger.error(str(err))
            abort(400, str(err))

        # noinspection PyUnboundLocalVariable
        rows, columns = collect_data(tlm_set, channel)
        params_list = collect_for_plot(rows, columns)
        app.logger.info(
            f"Building the plot for {channel} channel and {tlm_set.upper()} set"
        )
        filename = f"{channel.lower().replace('.', '_')}_{tlm_set}.png"
        path = os.path.join(app.instance_path, "plots")
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, filename)
        plot_telemetry(full_path, params_list, columns, channel)
        app.logger.info(f"Saved {filename}")

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
