"""
Application factory, configuration and URL description
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, abort, send_file, send_from_directory
from .upload import upload_file
from .ltu_db import init_app, get_db
from .subsets import subsets
from .plot import collect_for_plot, plot_telemetry

UPLOAD_FOLDER = "flask-telemetry-tool/tlm_app/"


def create_app(test_config=None):
    """
    Create and configure an instance of the Flask application.
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "ltu-tel.sqlite"),
        UPLOAD_FOLDER=UPLOAD_FOLDER,
    )

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

    # register the database commands
    init_app(app)

    @app.route("/")
    def tlm(name=None):
        return render_template("base.html", name=name)

    @app.route("/upload", methods=["GET", "POST"])
    def tlm_upload():
        return upload_file()

    @app.template_filter("dt")
    def to_time(timestamp):
        return datetime.fromtimestamp(timestamp)

    @app.template_filter("fmt")
    def represent_float(float_data):
        return f"{float_data:.3f}"

    def collect_data(subset, table):
        script = f"SELECT {','.join(subsets[subset])} FROM {table}"
        cursor_obj = get_db().cursor().execute(script)
        columns = [i[0] for i in cursor_obj.description]

        return cursor_obj, columns

    @app.route("/table")
    def view_table():
        table = request.args.get("set")
        subset = request.args.get("subset")

        if subset not in subsets:
            abort(400, f"No such subset '{subset}'")

        cursor_obj, columns = collect_data(subset, table)

        return render_template(
            "table.html",
            table=table,
            rows=cursor_obj,
            columns=columns,
            subset=subset,
        )

    @app.route("/plot")
    def view_plot():
        table = request.args.get("set")
        subset = request.args.get("subset")

        if subset not in subsets:
            abort(400, f"No such subset '{subset}'")

        cursor_obj, columns = collect_data(subset, table)
        params_list = collect_for_plot(cursor_obj)
        filename = "brd_tlm.png"
        full_path = os.path.join(app.instance_path, "plots", filename)
        plot_telemetry(full_path, params_list, columns)

        return render_template(
            "plot.html",
            filename=filename,
        )

    @app.route("/plot/<filename>")
    def show_plot(filename):
        filename = "brd_tlm.png"
        full_path = os.path.join(app.instance_path, "plots", filename)
        return send_file(full_path, mimetype="image/png")

    return app
