"""
Uploading LTU traces
"""

from typing import BinaryIO, cast
from flask import flash, request, render_template, current_app
from .packet import get_telemetry

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
            msg = "No file part"
            flash(msg, "error")
            current_app.logger.error(msg)

        elif (file := request.files["file"]).filename == "":
            msg = "No selected file"
            flash(msg, "error")
            current_app.logger.error(msg)

        elif file and allowed_file(file.filename):
            count = get_telemetry(cast(BinaryIO, file))

            msg = f"The file '{file.filename}' has been successfully uploaded"
            current_app.logger.info(msg)
            flash(msg, "success")
            flash(f"Read {count} packets", "info")
            current_app.logger.info(f"Added {count} packets to the database")

        else:
            msg = "Wrong extension (expected *.tld)"
            flash(msg, "error")
            current_app.logger.error(msg)

    return render_template("upload.html")
