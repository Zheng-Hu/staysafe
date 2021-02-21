"""
StaySafe following page view.

URLs include:
/u/<username>/following
"""
import flask
import staysafe
from staysafe.views.followers import check_user_and_method


def is_following(logname, username):
    """Return whether logname follows username."""
    # Connect to database
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT username1, username2 FROM following "
        "WHERE username1=? AND username2=?",
        (logname, username,)
    )
    if cur.fetchone():
        return True
    return False


@staysafe.app.route('/u/<username>/following/', methods=['GET', 'POST'])
def show_following(username):
    """Display /u/<username>/following/ route."""
    # Check if logged in
    if flask.session.get("username"):
        logname = flask.session["username"]
    else:
        return flask.redirect(flask.url_for("show_login"))

    check_user_and_method(username, logname)

    context = {"username": username,
               "logname": logname,
               "following": []}

    # Connect to database
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT users.username, users.filename "
        "FROM users, following "
        "WHERE following.username1=? "
        "AND users.username = following.username2", (username,)
    )
    following_info = cur.fetchall()

    for following in following_info:
        context["following"].append({
            "username": following["username"],
            "user_img_url": "/uploads/" + following["filename"],
            "logname_follows_username":
            is_following(logname, following["username"])
        })

    return flask.render_template("following.html", **context)
