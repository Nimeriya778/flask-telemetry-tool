"""
Uploading LTU traces
"""

from typing import BinaryIO, cast
from flask import flash, request, render_template
from .packet import get_telemetry
from .ltu_db import drop_table, create_table, insert_into_table, get_db

ALLOWED_EXTENSIONS = {"tld"}


def allowed_file(filename):
    """
    Check if an extension is valid.
    """

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    """
    Upload the file and redirects the user to the URL for the uploaded file.
    Check if the post request has the file part. If the user does not select a file,
    the browser submits an empty file without a filename.
    """

    if request.method == "POST":

        if "file" not in request.files:
            flash("No file part", "error")

        elif (file := request.files["file"]).filename == "":
            flash("No selected file", "error")

        elif file and allowed_file(file.filename):
            tlm, count = get_telemetry(cast(BinaryIO, file))

            conn = get_db()
            drop_table(conn, tlm)
            create_table(conn, tlm)
            insert_into_table(conn, tlm)
            conn.commit()

            flash("Your file has been successfully uploaded!", "success")
            flash(f"Read {count} packets.", "info")

        else:
            flash("Wrong extension (expected *.tld)", "error")

    return render_template("upload.html")
