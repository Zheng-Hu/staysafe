"""
StaySafe logout page view.

URLs include:
/accounts/logout/
"""
from flask import session, redirect, url_for
import staysafe


@staysafe.app.route('/accounts/logout/', methods=['POST'])
def show_logout():
    """Display /accounts/logout/ route."""
    session.pop('username', None)
    return redirect(url_for('show_login'))
