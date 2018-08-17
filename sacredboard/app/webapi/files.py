"""
Accessing the files.
"""
from flask import Blueprint, current_app, send_file

from sacredboard.app.data import NotFoundError
import bson
from enum import Enum
import io
import os
import mimetypes
import zipfile


files = Blueprint("files", __name__)


class _FileType(Enum):
    ARTIFACT = 1
    SOURCE = 2


_filetype_suffices = {
    _FileType.ARTIFACT: "artifact",
    _FileType.SOURCE: "source",
}


def get_file(file_id: str):
    """
    Get a specific file from GridFS.

    Returns a binary stream response or HTTP 404 if not found.
    """
    data = current_app.config["data"]  # type: DataStorage
    dao = data.get_files_dao()
    oid = bson.ObjectId(file_id)
    file = dao.get(oid)

    basename = os.path.basename(file.filename)
    _, ext = os.path.splitext(basename)

    if ext not in mimetypes.types_map:
        # unknown type
        mime = "binary/octet-stream"
    else:
        mime = mimetypes.types_map[ext]

    return send_file(file, mimetype=mime, attachment_filename=basename, as_attachment=True)


def get_files_zip(run_id: int, filetype: _FileType):
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
            oid = bson.ObjectId(file_id)
            file = dao_files.get(oid)
            data = zipfile.ZipInfo(file.filename)
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, file.read())
    memory_file.seek(0)

    fn_suffix = _filetype_suffices(filetype)
    return send_file(memory_file, attachment_filename=f'run{run_id}_{fn_suffix}.zip', as_attachment=True)


@files.route("/api/file/<string:file_id>")
def api_file(file_id):
    return get_file(file_id)


@files.route("/api/artifacts/<int:run_id>")
def api_artifacts(run_id):
    return get_files_zip(run_id, _FileType.ARTIFACT)


@files.route("/api/sources/<int:run_id>")
def api_sources(run_id):
    return get_files_zip(run_id, _FileType.SOURCE)


@files.errorhandler(NotFoundError)
def handle_not_found_error(e):
    """Handle exception when a metric is not found."""
    return "Couldn't find resource:\n%s" % e, 404


def initialize(app, app_config):
    """Register the module in Flask."""
    app.register_blueprint(files)
