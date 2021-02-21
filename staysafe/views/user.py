"""
StaySafe user page view.

URLs include:
/u/<username>/
"""
import pathlib
import uuid
import flask
import staysafe
from staysafe.views.followers import user_exists, check_methods
from staysafe.views.following import is_following


def get_fullname(username):
    """Return fullname of the username."""
    # Connect to database
    connection = staysafe.model.get_db()

    cur = connection.execute(
        "SELECT fullname FROM users "
        "WHERE username=?", (username,)
    )

    return cur.fetchone()["fullname"]


def count_following(username):
    """Return the number of followings of the user."""
    # Connect to database
    connection = staysafe.model.get_db()

    cur = connection.execute(
        "SELECT COUNT(*) FROM following "
        "WHERE username1=?", (username,)
    )

    return cur.fetchone()["COUNT(*)"]


def count_followers(username):
    """Return the number of followers of the user."""
    # Connect to database
    connection = staysafe.model.get_db()

    cur = connection.execute(
        "SELECT COUNT(*) FROM following "
        "WHERE username2=?", (username,)
    )

    return cur.fetchone()["COUNT(*)"]


def count_posts(username):
    """Return the number of posts of the user."""
    # Connect to database
    connection = staysafe.model.get_db()

    cur = connection.execute(
        "SELECT COUNT(*) FROM posts "
        "WHERE owner=?", (username,)
    )

    return cur.fetchone()["COUNT(*)"]


@staysafe.app.route('/u/<username>/', methods=['GET', 'POST'])
def show_user(username):
    """Display /u/<username>/ route."""
    # Check if logged in
    if flask.session.get("username"):
        logname = flask.session["username"]
    else:
        return flask.redirect(flask.url_for("show_login"))
    # Check if user exists
    user_exists(username)

    # Check methods (follow, unfollow)
    check_methods(logname)

    if flask.request.method == 'POST':
        if "create_post" in flask.request.form:
            # Upload files
            # The next three lines are from Flask tutorial example
            if 'file' not in flask.request.files:
                flask.flash('No file part')
                return flask.redirect(flask.request.url)
            fileobj = flask.request.files["file"]
            filename = fileobj.filename
            # The next three lines are from Flask tutorial example
            if filename == '':
                flask.flash('No selected file')
                return flask.redirect(flask.request.url)
            if fileobj and (filename.rsplit('.')[1].lower() in
                            staysafe.config.ALLOWED_EXTENSIONS):
                uuid_basename = "{stem}{suffix}".format(
                    stem=uuid.uuid4().hex,
                    suffix=pathlib.Path(filename).suffix
                )
                path = staysafe.app.config["UPLOAD_FOLDER"]/uuid_basename
                fileobj.save(path)
            # store filename in data.sql
            connection = staysafe.model.get_db()
            connection.execute(
                "INSERT INTO posts(filename, owner)"
                "VALUES (?, ?)", (uuid_basename, username,)
            )

    context = {
        "logname": logname,
        "username": username,
        "logname_follows_username": is_following(logname, username),
        "fullname": get_fullname(username),
        "following": count_following(username),
        "followers": count_followers(username),
        "total_posts": count_posts(username),
        "posts": []
    }

    # Connect to database
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT postid, filename FROM posts "
        "WHERE owner = ? "
        "ORDER BY postid DESC", (username,)
    )
    posts_info = cur.fetchall()

    for post in posts_info:
        context["posts"].append({
            "postid": post["postid"],
            "img_url": "/uploads/" + post["filename"]
        })

    return flask.render_template("user.html", **context)
