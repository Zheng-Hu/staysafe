"""
StaySafe delete user page view.

URLs include:
/accounts/delete/
"""
import os
from flask import session, redirect, url_for, request, render_template
import staysafe


@staysafe.app.route('/accounts/delete/', methods=['GET', 'POST'])
def show_delete():
    """Display /accounts/delete/ route."""
    if 'username' in session:
        logname = session['username']
    else:
        return redirect(url_for('show_login'))
    context = {"username": logname}

    if request.method == 'POST':
        connection = staysafe.model.get_db()
        # Delete user icon
        cur = connection.execute(
            "SELECT filename FROM users WHERE username = ?", (logname,)
        )
        user_icon = cur.fetchall()
        filename = user_icon[0]['filename']
        filepath = staysafe.app.config["UPLOAD_FOLDER"]/filename
        os.remove(filepath)

        # Delete all posts from user
        cur1 = connection.execute(
            "SELECT filename FROM posts WHERE owner = ?", (logname,)
        )
        user_posts = cur1.fetchall()
        for one_post in user_posts:
            imgname = one_post['filename']
            imgpath = staysafe.app.config["UPLOAD_FOLDER"]/imgname
            os.remove(imgpath)

        # Remove all ralevent entries in database
        connection.execute(
            "DELETE FROM users WHERE username = ?", (logname,)
        )
        session.pop('username', None)
        return redirect(url_for('show_create'))

    return render_template("delete.html", **context)
