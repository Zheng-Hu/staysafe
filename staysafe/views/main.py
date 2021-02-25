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
    if flask.request.method == 'POST':
        return flask.redirect(flask.url_for('show_Duder'))
    return flask.render_template("main.html")

@staysafe.app.route('/Duder/', methods=['GET', 'POST'])
def show_Duder():
    return flask.render_template("DuderLibrary.html")
