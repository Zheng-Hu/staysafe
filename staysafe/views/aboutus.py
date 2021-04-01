"""
StaySafe index view.
URLs include:
/aboutus/
"""
import flask
from flask import session #, request
import arrow
import staysafe
import logging
import sys
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('werkzeug')

@staysafe.app.route('/aboutus/', methods=['GET', 'POST'])
def show_aboutus():
    return flask.render_template("aboutus.html")