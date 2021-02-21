"""
StaySafe logout page view.

URLs include:
/accounts/logout/
"""

from flask import session, redirect, url_for, request, render_template
import staysafe


@staysafe.app.route('/explore/', methods=['POST', 'GET'])
def show_explore():
    """Display /accounts/logout/ route."""
    # if not logged in, redirect to /account/login/
    if 'username' not in session:
        return redirect(url_for('show_login'))
    # Get to database
    connection = staysafe.model.get_db()
    logname = session['username']
    if request.method == 'POST':
        if 'follow' in request.form:
            connection.execute("INSERT INTO following (username1, username2) "
                               "VALUES (?, ?)",
                               (logname, request.form['username'],))
    # Get all users
    all_user = connection.execute("SELECT username, filename "
                                  "FROM users")
    all_user = all_user.fetchall()
    # Get users that this user followe
    followers = connection.execute("SELECT username2 "
                                   "FROM following WHERE username1 = ?",
                                   (logname,))
    followers = followers.fetchall()
    follow = []
    nfollow = []
    for follower in followers:
        follow.append(follower['username2'])
    for a_user in all_user:
        if (a_user['username'] not in follow) and \
           (a_user['username'] != logname):
            img_url = "/uploads/" + str(a_user['filename'])
            dic_nfowllow = {"username": a_user['username'],
                            "user_img_url": img_url}
            nfollow.append(dic_nfowllow)
    context = {"logname": logname, "not_following": nfollow}
    return render_template("explore.html", **context)
