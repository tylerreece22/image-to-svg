import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from src.image_to_svg import convert_image_to_svg

UPLOAD_FOLDER = (
    "/Users/tylerreece/Development/temp/python-practice-server/flask_app/uploads"
)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.debug(f"filename {filename}")
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            new_filename = filename.split(".")[0] + ".svg"
            app.logger.debug(f"new_filename {new_filename}")

            # convert and save svg file
            convert_image_to_svg(
                os.path.join(app.config["UPLOAD_FOLDER"], filename),
                os.path.join(app.config["UPLOAD_FOLDER"], new_filename),
            )
            return redirect(url_for("download_file", name=new_filename))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
