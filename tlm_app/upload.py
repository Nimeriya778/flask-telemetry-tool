"""
Uploading LTU traces
"""

import os
from flask import flash, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

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
            flash("No file part")

            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

            return redirect(url_for("download_file", name=filename))

    return redirect(request.url)
