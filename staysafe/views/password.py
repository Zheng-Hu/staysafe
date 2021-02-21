"""
SatySafe modify password page view.

URLs include:
/accounts/password/
"""
import uuid
import hashlib
from flask import session, redirect, url_for, request, abort, render_template
import staysafe


@staysafe.app.route('/accounts/password/', methods=['GET', 'POST'])
def show_password():
    """Display /accounts/password/ route."""
    if 'username' in session:
        logname_p = session['username']
    else:
        return redirect(url_for('show_login'))

    if request.method == 'POST':
        # Check if old password is correct
        connection = staysafe.model.get_db()
        cur = connection.execute(
            "SELECT password FROM users "
            "WHERE username = ?", (logname_p,)
        )
        password_db = cur.fetchall()
        old_password = password_db[0]['password']
        element = old_password.split("$")
        old_salt = element[1]
        input_password = request.form['password']
        hash_input_password = hashing(input_password, old_salt)

        if hash_input_password != old_password:
            abort(403)
        if request.form['new_password1'] != request.form['new_password2']:
            abort(401)

        # Modify password in database
        new_password = request.form['new_password1']
        hash_new_password = hashing(new_password, uuid.uuid4().hex)
        connection.execute(
            "UPDATE users SET password = ? "
            "WHERE username = ?", (hash_new_password, logname_p,)
        )

        return redirect(url_for('show_edit'))

    context = {"username": logname_p}

    return render_template("password.html", **context)


def hashing(password, salt):
    """Hash the password."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string
