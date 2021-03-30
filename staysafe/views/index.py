"""
StaySafe index view.
URLs include:
/
"""
import flask
from flask import session
import arrow
import staysafe


@staysafe.app.route('/', methods=['GET', 'POST'])
def show_index():
    return flask.render_template("index.html")

@staysafe.app.route('/Duder/', methods=['GET', 'POST'])
def show_Duder():
    return flask.render_template("DuderLibrary.html")