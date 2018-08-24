"""Accessing the files."""
from enum import Enum
import io
import os
import mimetypes
import zipfile

from flask import Blueprint, current_app, render_template, send_file, Response

from sacredboard.app.data import NotFoundError


files = Blueprint("files", __name__)


class _FileType(Enum):
    ARTIFACT = 1
    SOURCE = 2


_filetype_suffices = {
    _FileType.ARTIFACT: "artifact",
    _FileType.SOURCE: "source",
}


def _get_binary_info(binary: bytes):
    hex_data = ""
    for i in range(0, 10):
        if i > 0:
            hex_data += " "
        hex_data += hex(binary[i])
    hex_data += " ..."
    return "Binary data\nLength: {}\nFirst 10 bytes: {}".format(len(binary), hex_data)


def get_file(file_id: str, download):
    """
    Get a specific file from GridFS.

    Returns a binary stream response or HTTP 404 if not found.
    """
    data = current_app.config["data"]  # type: DataStorage
    dao = data.get_files_dao()
    file = dao.get(file_id)

    if download:
        mime = mimetypes.guess_type(file.filename)[0]
        if mime is None:
            # unknown type
            mime = "binary/octet-stream"

        basename = os.path.basename(file.filename)
        return send_file(file, mimetype=mime, attachment_filename=basename, as_attachment=True)
    else:
        rawdata = file.read()
        try:
            text = rawdata.decode('utf-8')
        except UnicodeDecodeError:
            # not decodable as utf-8
            text = _get_binary_info(rawdata)
        html = render_template("api/file_view.html", content=text)
        return Response(html)


def get_files_zip(run_id: int, filetype: _FileType):
    """Send all artifacts or sources of a run as ZIP."""
    data = current_app.config["data"]
    dao_runs = data.get_run_dao()
    dao_files = data.get_files_dao()
    run = dao_runs.get(run_id)

    if filetype == _FileType.ARTIFACT:
        target_files = run['artifacts']
    elif filetype == _FileType.SOURCE:
        target_files = run['experiment']['sources']
    else:
        raise Exception("Unknown file type: %s" % filetype)

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for f in target_files:
            # source and artifact files use a different data structure
            file_id = f['file_id'] if 'file_id' in f else f[1]
            file = dao_files.get(file_id)
            data = zipfile.ZipInfo(file.filename, date_time=file.upload_date.timetuple())
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, file.read())
    memory_file.seek(0)

    fn_suffix = _filetype_suffices[filetype]
    return send_file(memory_file, attachment_filename='run{}_{}.zip'.format(run_id, fn_suffix), as_attachment=True)


@files.route("/api/file/<string:file_id>")
def api_file(file_id):
    """Download a file."""
    return get_file(file_id, True)


@files.route("/api/fileview/<string:file_id>")
def api_fileview(file_id):
    """View a file."""
    return get_file(file_id, False)


@files.route("/api/artifacts/<int:run_id>")
def api_artifacts(run_id):
    """Download all artifacts of a run as ZIP."""
    return get_files_zip(run_id, _FileType.ARTIFACT)


@files.route("/api/sources/<int:run_id>")
def api_sources(run_id):
    """Download all sources of a run as ZIP."""
    return get_files_zip(run_id, _FileType.SOURCE)


@files.errorhandler(NotFoundError)
def handle_not_found_error(e):
    """Handle exception when a metric is not found."""
    return "Couldn't find resource:\n%s" % e, 404


def initialize(app, app_config):
    """Register the module in Flask."""
    app.register_blueprint(files)
