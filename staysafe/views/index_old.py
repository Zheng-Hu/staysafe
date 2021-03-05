"""
StaySafe index (main) view.

URLs include:
/
"""
import flask
from flask import session
import arrow
import staysafe


@staysafe.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    # check if logged in
    if 'username' not in session:
        return flask.redirect(flask.url_for('show_login'))
    # else logged in
    logname = session['username']
    # Connect to database
    connection = staysafe.model.get_db()
    if flask.request.method == 'POST':
        if "like" in flask.request.form:
            connection.execute("INSERT INTO likes (owner, postid) "
                               "VALUES (?, ?)",
                               (logname, flask.request.form['postid'], ))
        if "unlike" in flask.request.form:
            connection.execute("DELETE FROM likes "
                               "WHERE owner = ? AND postid = ?",
                               (logname, flask.request.form['postid'], ))
        if "comment" in flask.request.form:
            connection.execute("INSERT INTO comments (owner, postid, text) "
                               "VALUES (?, ?, ?)",
                               (logname, flask.request.form['postid'],
                                flask.request.form['text'], ))
    posts = []
    # Query database for post id
    cur = connection.execute(
        "SELECT posts.postid FROM posts, following "
        "WHERE following.username1 = ? AND posts.owner = following.username2 "
        "UNION "
        "SELECT postid FROM posts WHERE owner = ?", (logname, logname, )
    )
    # sort postid in descending order
    id_dic = sorted(cur.fetchall(), key=lambda x: x['postid'], reverse=True)
    # make the config.json like p1
    for id_d in id_dic:
        # for each post add postid
        post = id_d
        # add owner
        cur = connection.execute("SELECT owner FROM posts "
                                 "WHERE postid = ?", (id_d['postid'],))
        owner = cur.fetchall()
        owner = owner[0]['owner']
        post['owner'] = owner
        # add owner_img_url
        cur = connection.execute("SELECT filename FROM users "
                                 "WHERE username = ?", (owner, ))
        owner_img = cur.fetchall()
        owner_img = owner_img[0]['filename']
        post['owner_img_url'] = "/uploads/" + str(owner_img)
        # add img_url
        cur = connection.execute("SELECT filename FROM posts "
                                 "WHERE postid = ?", (id_d['postid'],))
        post['img_url'] = "/uploads/" + cur.fetchall()[0]['filename']
        # add timestamp
        cur = connection.execute("SELECT created FROM posts "
                                 "WHERE postid = ?", (id_d['postid'],))
        timestamp = cur.fetchall()
        timestamp = arrow.get(timestamp[0]['created'])
        present = arrow.utcnow()
        timestamp = timestamp.humanize(present)
        post['timestamp'] = timestamp
        # add likes
        cur = connection.execute("SELECT COUNT(owner) FROM likes "
                                 "WHERE postid = ?", (id_d['postid'],))
        post['likes'] = cur.fetchall()[0]['COUNT(owner)']
        # add comments
        cur = connection.execute("SELECT text, owner FROM comments "
                                 "WHERE postid = ?", (id_d['postid'],))
        post['comments'] = cur.fetchall()
        # whether it should be like button or unlike button
        # False -- like
        # True -- unlike
        cur = connection.execute("SELECT * FROM likes "
                                 "WHERE postid = ? AND owner = ? "
                                 "ORDER BY postid ASC",
                                 (id_d['postid'], logname,))
        like_or_not = cur.fetchall()
        like_bool = False
        if like_or_not == []:
            like_bool = False
        else:
            like_bool = True
        post['like_bool'] = like_bool
        # add post to the list of posts
        posts.append(post)
    # Add database info to context
    context = {"logname": logname, "posts": posts}
    return flask.render_template("index.html", **context)
