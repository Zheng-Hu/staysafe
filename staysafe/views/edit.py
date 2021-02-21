"""
StaySafe edit user page view.

URLs include:
/accounts/edit/
"""
import os
import pathlib
import uuid
from flask import session, redirect, url_for, request, render_template
import staysafe


@staysafe.app.route('/accounts/edit/', methods=['GET', 'POST'])
def show_edit():
    """Display /accounts/edit/ route."""
    if 'username' in session:
        logname = session['username']
    else:
        return redirect(url_for('show_login'))

    if request.method == 'POST':
        connection = staysafe.model.get_db()
        # Check file
        fileobj = request.files["file"]
        if fileobj:
            cur = connection.execute(
                "SELECT * FROM users WHERE username = ?", (logname,)
            )
            info = cur.fetchall()
            old_filepath = \
                staysafe.app.config["UPLOAD_FOLDER"]/info[0]['filename']
            os.remove(old_filepath)
            new_filename = fileobj.filename
            new_uuid_basename = "{stem}{suffix}".format(
                stem=uuid.uuid4().hex,
                suffix=pathlib.Path(new_filename).suffix
            )
            # Save to disk
            new_path = staysafe.app.config["UPLOAD_FOLDER"]/new_uuid_basename
            fileobj.save(new_path)

            # Also update name of file in database
            connection.execute(
                "UPDATE users SET filename = ? "
                "WHERE username = ?", (new_uuid_basename, logname, )
            )

        # Modify fullname and email in database
        new_fullname = request.form['fullname']
        new_email = request.form['email']
        connection.execute(
            "UPDATE users SET fullname = ?, email = ? "
            "WHERE username = ?", (new_fullname, new_email, logname, )
        )

    # Fill in the form
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?", (logname,)
    )
    logname_info = cur.fetchall()
    filename = logname_info[0]['filename']
    filepath = "/uploads/" + filename
    context = {"username": logname_info[0]['username'],
               "fullname": logname_info[0]['fullname'],
               "email": logname_info[0]['email'],
               "filepath": filepath}

    return render_template("edit.html", **context)
