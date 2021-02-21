"""
StaySafe create user page view.

URLs include:
/accounts/create/
"""
import pathlib
import uuid
from flask import session, redirect, url_for, request, abort, render_template
import staysafe
from staysafe.views.password import hashing


@staysafe.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Display /accounts/create/ route."""
    if "user" in session:
        return redirect(url_for('show_edit'))

    if request.method == 'POST':
        # Check if username already exist
        username = request.form["username"]
        connection = staysafe.model.get_db()
        cur = connection.execute(
            "SELECT username FROM users"
        )
        all_users = cur.fetchall()
        for one_user in all_users:
            if one_user["username"] == username:
                abort(409)

        # Check if password is empty
        password = request.form["password"]
        if password == '':
            abort(400)

        # Check file
        fileobj = request.files["file"]
        if not fileobj:
            abort(400)
        filename = fileobj.filename
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix
        )
        # Save to disk
        path = staysafe.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        fullname = request.form["fullname"]
        email = request.form["email"]
        # Save user info to database
        cur = connection.execute(
            "INSERT INTO users(username, fullname, email, filename, password) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, fullname, email, uuid_basename,
             hashing(password, uuid.uuid4().hex))
        )

        # Log the user in
        session['username'] = username
        return redirect(url_for('show_index'))
    return render_template("create.html")
