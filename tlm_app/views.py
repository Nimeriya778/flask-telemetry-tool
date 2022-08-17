"""
Application factory, configuration and URL description
"""

import os
from flask import Flask, render_template, request, redirect
from .upload import upload_file
from .ltu_db import init_app, get_db
from .subsets import subsets

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

    @app.route("/table")
    def view_table():
        table = request.args.get("set")
        subset = request.args.get("subset")

        if subset not in subsets:
            return redirect("/")

        script = f"SELECT {','.join(subsets[subset])} FROM {table}"

        cursor_obj = get_db().cursor().execute(script)
        columns = [i[0] for i in cursor_obj.description]

        return render_template(
            "table.html",
            table=table,
            rows=cursor_obj,
            columns=columns,
            subset=subset,
        )

    return app
