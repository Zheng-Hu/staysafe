"""
StaySafe follower page view.

URLs include:
/u/<username>/follower
"""
import flask
import staysafe


def has_follower(logname, username):
    """Return whether logname has a follower username."""
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT username1, username2 FROM following "
        "WHERE username1=? AND username2=?",
        (username, logname,)
    )
    if cur.fetchone():
        return True
    return False


def user_exists(username):
    """Return True if username exists in database, abort otherwise."""
    # Query database
    cur = (staysafe.model.get_db()).execute(
        "SELECT username "
        "FROM users"
    )
    all_users = cur.fetchall()

    for user in all_users:
        if username == user["username"]:
            return True
    return flask.abort(404)


def check_methods(logname):
    """Check POST method."""
    if flask.request.method == 'POST':
        if "follow" in flask.request.form:
            # Insert the relationship to following
            connection = staysafe.model.get_db()
            connection.execute(
                "INSERT INTO following(username1, username2) "
                "VALUES (?, ?)", (logname, flask.request.form["username"],)
            )
        if "unfollow" in flask.request.form:
            # Delete the relationship in following
            connection = staysafe.model.get_db()
            connection.execute(
                "DELETE FROM following "
                "WHERE username1=? AND username2=?",
                (logname, flask.request.form["username"],)
            )


def check_user_and_method(username, logname):
    """Check username and methods."""
    result = user_exists(username)
    check_methods(logname)
    return result


@staysafe.app.route('/u/<username>/followers/', methods=['GET', 'POST'])
def show_follower(username):
    """Display /u/<username>/followers/ route."""
    if 'username' in flask.session:
        logname = flask.session['username']
    else:
        return flask.redirect(flask.url_for("show_login"))

    check_user_and_method(username, logname)

    context = {"logname": logname,
               "username": username,
               "followers": []}

    # Connect to database
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT users.username, users.filename "
        "FROM users, following "
        "WHERE following.username2=? AND "
        "users.username = following.username1", (username,)
    )
    followers_info = cur.fetchall()

    for follower in followers_info:
        context["followers"].append({
            "username": follower["username"],
            "user_img_url": "/uploads/" + follower["filename"],
            "logname_follows_username":
            has_follower(follower["username"], logname)
        })

    return flask.render_template("followers.html", **context)
