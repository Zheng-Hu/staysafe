"""
staysafe prediction page view.

URLs include:
/predict/
"""
import os
import flask
import staysafe

@staysafe.app.route('/predict.html', methods=['GET', 'POST'])
def show_prediction():
    connection = staysafe.model.get_db()
    if flask.request.method == 'POST':
        # if "specific" in flask.request.form:
        cur_building_info = connection.execute("SELECT id, building_name "
                                               "FROM buildings WHERE building_name=?",
                                               (flask.request.form['building_name'],))
        id_name = cur_building_info.fetchone()
        selected_id = id_name["id"]
        selected_name = id_name["building_name"]

        # print("print id_name:", id_name)
        # print("print id:", selected_id)
        # print("print name:", selected_name)

        cur_time_info = connection.execute("SELECT cong_level "
                                           "FROM congestion WHERE owner_id=? "
                                           "AND day_of_week=? "
                                           "AND time_period=?",
                                           (selected_id,
                                           flask.request.form["day_of_week"],
                                           flask.request.form["time_period"],))

        selected_cong_level = cur_time_info.fetchone()["cong_level"]
        selected_day_of_week = flask.request.form["day_of_week"]
        selected_time_period = flask.request.form["time_period"]

        # print("selected_cong_level:", selected_cong_level)
        context = {"building_name": selected_name,
                   "day_of_week": selected_day_of_week,
                   "time_period": selected_time_period,
                   "cong_level": selected_cong_level}

        return flask.render_template("predict.html", **context)