"""
StaySafe index view.
URLs include:
/
"""
import flask
from flask import session, request
import arrow
import staysafe


@staysafe.app.route('/', methods=['GET', 'POST'])
def show_index():
    # if flask.request.method == 'POST':
    #     return flask.redirect(flask.url_for('show_Duder'))
    # return flask.render_template("main.html")
    # Get to database
    connection = staysafe.model.get_db()
    # if flask.request.method == 'POST':
    # specific: search a certain building FRONTEND-FIXME
    # if "specific" in request.form:
    building_info = connection.execute("SELECT id, building_name "
                                        "FROM buildings WHERE building_name=?",
                                        (flask.request.form['building_name'],))
    # general: search a group of buildings FRONTEND-FIXME
    # if "general" in request.form:
    # will develop in beta release FIXME
    time_info = connection.execute("SELECT cong_level "
                                    "FROM congestion WHERE owner_id=? "
                                    "AND day_of_week=? "
                                    "AND time_period=?",
                                    (building_info["id"],
                                    flask.request.form["day_of_week"],
                                    flask.request.form["time_period"],))

    # FRONTEND-FIXME: templates need to use the exactly same names to fetch the info
    context = {"building_name": building_info["building_name"],
                "day_of_week": time_info["day_of_week"],
                "time_period": time_info["time_period"]}

    return flask.render_template("predict.html", **context)


@staysafe.app.route('/Duder/', methods=['GET', 'POST'])
def show_Duder():
    return flask.render_template("DuderLibrary.html")

@staysafe.app.route('/', methods=['GET', 'POST'])
def show_Predict():
    # Get to database
    connection = staysafe.model.get_db()
    # if flask.request.method == 'POST':
    # specific: search a certain building FRONTEND-FIXME
    if "specific" in request.form:
        building_info = connection.execute("SELECT id, building_name "
                                            "FROM buildings WHERE building_name=?",
                                            (flask.request.form['building_name'],))
    # general: search a group of buildings FRONTEND-FIXME
    # if "general" in request.form:
    # will develop in beta release FIXME
    time_info = connection.execute("SELECT cong_level "
                                    "FROM congestion WHERE owner_id=? "
                                    "AND day_of_week=? "
                                    "AND time_period=?",
                                    (building_info["id"],
                                    flask.request.form["day_of_week"],
                                    flask.request.form["time_period"],))

    # FRONTEND-FIXME: templates need to use the exactly same names to fetch the info
    context = {"building_name": building_info["building_name"],
                "day_of_week": time_info["day_of_week"],
                "time_period": time_info["time_period"]}

    return flask.render_template("predict.html", **context)
