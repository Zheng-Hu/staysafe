"""
StaySafe login page view.

URLs include:
/accounts/login/
"""
import hashlib
import flask
from flask import session, abort
import staysafe


@staysafe.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Display /accounts/login/ route."""
    # Check if logged in
    if 'username' in session:
        return flask.redirect(flask.url_for('show_index'))
    # if not logged in
    if flask.request.method == 'POST':
        logname = flask.request.form['username']
        password = flask.request.form['password']

        # Get to database
        connection = staysafe.model.get_db()
        curl = connection.execute(
            "SELECT password FROM users "
            "WHERE username = ?", (logname,)
        )
        # hashed password in database
        password_db_might = curl.fetchall()

        # if the username is not in the database, abort
        if not password_db_might:
            abort(403)
        else:
            # assume that no duplicated username
            password_db = password_db_might[0]['password']
        algo, salt, hashing = str(password_db).split("$")
        # encrpt the enter password
        hash_obj = hashlib.new(algo)
        password_salted_input = salt + password
        hash_obj.update(password_salted_input.encode('utf-8'))
        password_hash_new = hash_obj.hexdigest()
        # if password incorrect, abort
        if hashing != password_hash_new:
            abort(403)
        session['username'] = logname
        # redirect to
        return flask.redirect(flask.url_for('show_index'))

    return flask.render_template("login.html")
