"""
StaySafe uploaded image page view.

URLs include:
/uploads/<filename>
"""
from flask import session, abort
import flask
import staysafe


@staysafe.app.route('/uploads/<filename>')
def show_upload(filename):
    """Display /uploads/<filename> route."""
    if 'username' not in session:
        abort(403)
    return flask.send_from_directory(staysafe.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)
