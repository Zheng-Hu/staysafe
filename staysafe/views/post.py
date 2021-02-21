"""
StaySafe post page view.

URLs include:
/p/<postid>/
"""
import os
import flask
import arrow
import staysafe


def get_logname_likes_post(logname, postid):
    """Return ture if logname like the post, false otherwise."""
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT owner, postid FROM likes "
        "WHERE owner=? AND postid=?", (logname, postid,)
    )
    if cur.fetchone():
        return True
    return False


def get_username(postid):
    """Return username of the post."""
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT owner FROM posts "
        "WHERE postid=?", (postid, )
    )
    return cur.fetchone()["owner"]


def get_user_filename(username):
    """Return filename of the user."""
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT filename FROM users "
        "WHERE username=?", (username,)
    )
    return cur.fetchone()["filename"]


def get_timestamp(postid):
    """Return timestamp of the post."""
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT created FROM posts "
        "WHERE postid=?", (postid,)
    )
    timestamp = arrow.get(cur.fetchall()[0]["created"])
    present = arrow.utcnow()
    return timestamp.humanize(present)


def count_likes(postid):
    """Return the number of likes of given post."""
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT COUNT(*) FROM likes "
        "WHERE postid=?", (postid,)
    )
    return cur.fetchone()["COUNT(*)"]


def get_comment_owner(commentid):
    """Return the owner username of the comment."""
    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT owner FROM comments "
        "WHERE commentid=?", (commentid,)
    )
    return cur.fetchone()["owner"]


@staysafe.app.route('/p/<postid>/', methods=['GET', 'POST'])
def show_post(postid):
    """Display /p/<postid>/ route."""
    # Check if logged in
    if flask.session.get("username"):
        logname = flask.session["username"]
    else:
        return flask.redirect(flask.url_for("show_login"))

    username = get_username(postid)

    if flask.request.method == 'POST':
        if "like" in flask.request.form:
            connection = staysafe.model.get_db()
            connection.execute(
                "INSERT INTO likes (owner, postid) "
                "VALUES (?, ?)", (logname, postid,)
            )
        if "unlike" in flask.request.form:
            connection = staysafe.model.get_db()
            connection.execute(
                "DELETE FROM likes "
                "WHERE owner=? AND postid=?", (logname, postid,)
            )
        if "comment" in flask.request.form:
            connection = staysafe.model.get_db()
            connection.execute(
                "INSERT INTO comments (owner, postid, text) "
                "VALUES (?, ?, ?)",
                (logname, postid, flask.request.form['text'],)
            )
        if "uncomment" in flask.request.form:
            if logname != get_comment_owner(flask.request.form['commentid']):
                flask.abort(403)
            connection = staysafe.model.get_db()
            connection.execute(
                "DELETE FROM comments "
                "WHERE commentid=?",
                (flask.request.form['commentid'],)
            )
            print(flask.request.form['commentid'])
        if "delete" in flask.request.form:
            if logname != username:
                flask.abort(403)
            connection = staysafe.model.get_db()
            cur = connection.execute(
                "SELECT filename FROM posts "
                "WHERE postid=?",
                (postid,)
            )
            imgname = cur.fetchone()["filename"]
            imgpath = staysafe.app.config["UPLOAD_FOLDER"]/imgname
            connection.execute(
                "DELETE FROM posts "
                "WHERE postid=? AND owner=?",
                (postid, logname,)
            )
            os.remove(imgpath)

    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT filename, owner FROM posts "
        "WHERE postid=?", (postid,)
    )
    post_info = cur.fetchone()
    if not post_info:
        return flask.redirect(flask.url_for("show_user", username=username))

    context = {
        "logname": logname,
        "postid": postid,
        # This is new (not in config.json in p1)
        "logname_likes_post": get_logname_likes_post(logname, postid),
        "owner": post_info["owner"],
        "owner_img_url": "/uploads/" + get_user_filename(post_info["owner"]),
        "img_url": "/uploads/" + post_info["filename"],
        "timestamp": get_timestamp(postid),
        "likes": count_likes(postid),
        "comments": []
    }

    connection = staysafe.model.get_db()
    cur = connection.execute(
        "SELECT commentid, owner, text FROM comments "
        "WHERE postid=? "
        "ORDER BY commentid ASC", (postid,)
    )
    comments_info = cur.fetchall()

    for comment in comments_info:
        context["comments"].append({
            "owner": comment["owner"],
            "commentid": comment["commentid"],
            "text": comment["text"]
        })

    return flask.render_template("post.html", **context)
