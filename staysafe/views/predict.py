"""
staysafe prediction page view.
Mainly developed by QX; Partially adapted by JD
URLs include:
/predict/
"""
import os
import flask
import staysafe
import sys

@staysafe.app.route('/predict.html', methods=['GET', 'POST'])
def show_prediction():
    connection = staysafe.model.get_db()
    if flask.request.method == 'POST':
        # Invalid input: too long
        if (len(flask.request.form['building']) > 63):
            return flask.render_template("error.html")

        if flask.request.form['mode'] == "building":
            cur_building_info = connection.execute("SELECT id, building_name, campus "
                                                "FROM buildings WHERE building_name LIKE :val",
                                                {'val': '%' + flask.request.form["building"] + '%'})
            id_names = cur_building_info.fetchall()
            print("id_names:", id_names)
            if id_names is None:
                return flask.render_template("error.html")

            if len(id_names) == 1:
                id_name = id_names[0]
                selected_id = id_name["id"]
                selected_name = id_name["building_name"]
                selected_campus = id_name["campus"]

                cur_cong_level = connection.execute("SELECT cong_level "
                                                "FROM congestion WHERE owner_id=? "
                                                "AND day_of_week=? "
                                                "AND time_period=?",
                                                (selected_id,
                                                flask.request.form["day"],
                                                flask.request.form["time"],))

                info = cur_cong_level.fetchone()

                selected_cong_level = info["cong_level"]
                busy_level = ""
                if (selected_cong_level < 0.25):
                    busy_level = "usually not busy (recommend going)"
                elif (selected_cong_level < 0.5):
                    busy_level = "usually not too busy"
                elif (selected_cong_level < 0.75):
                    busy_level = "usually a little busy"
                else:
                    busy_level = "usually busy (not recommend going)"
                selected_day_of_week = flask.request.form["day"]
                selected_time_period = flask.request.form["time"]

                context = {"id": str(selected_id) + '.jpg',
                        "name": selected_name,
                        "campus": selected_campus,
                        "day_of_week": selected_day_of_week,
                        "time_period": selected_time_period,
                        "cong_level": busy_level}
                print("result " + str(context), file=sys.stdout)
                sys.stdout.flush()

                return flask.render_template("predict.html", 
                                                graph='static/images/' + str(selected_id) + '.jpg', **context)
            else:
                selected_names_cong_levels = []
                for item in id_names:
                    cur_cong_level = connection.execute("SELECT cong_level "
                                                        "FROM congestion WHERE owner_id=? "
                                                        "AND day_of_week=? "
                                                        "AND time_period=?",
                                                        (item["id"],
                                                        flask.request.form["day"],
                                                        flask.request.form["time"],))
                    selected_cong_level = cur_cong_level.fetchone()["cong_level"]
                    busy_level = ""
                    if (selected_cong_level < 0.25):
                        busy_level = "usually not busy (recommend going)"
                    elif (selected_cong_level < 0.5):
                        busy_level = "usually not too busy"
                    elif (selected_cong_level < 0.75):
                        busy_level = "usually a little busy"
                    else:
                        busy_level = "usually busy (not recommend going)"
                    selected_names_cong_levels.append({
                        "name": item["building_name"],
                        "campus": item["campus"],
                        "cong_level": busy_level
                    })

                context = {"buildings_info": selected_names_cong_levels,
                            "day_of_week": flask.request.form["day"],
                            "time_period": flask.request.form["time"]}
                return flask.render_template("predict.html", **context)

        if flask.request.form['mode'] == "category":
            selected_names_cong_levels = []
            cur_category_info = connection.execute("SELECT id, building_name, category, campus "
                                                    "FROM buildings")
            id_name_category = cur_category_info.fetchall()
            for item in id_name_category:
                if flask.request.form["category"] in item["category"]:
                    cur_cong_level = connection.execute("SELECT cong_level "
                                                        "FROM congestion WHERE owner_id=? "
                                                        "AND day_of_week=? "
                                                        "AND time_period=?",
                                                        (item["id"],
                                                        flask.request.form["day"],
                                                        flask.request.form["time"],))
                    selected_cong_level = cur_cong_level.fetchone()["cong_level"]
                    busy_level = ""
                    if (selected_cong_level < 0.25):
                        busy_level = "usually not busy (recommend going)"
                    elif (selected_cong_level < 0.5):
                        busy_level = "usually not too busy"
                    elif (selected_cong_level < 0.75):
                        busy_level = "usually a little busy"
                    else:
                        busy_level = "usually busy (not recommend going)"
                    selected_names_cong_levels.append({
                        "name": item["building_name"],
                        "campus": item["campus"],
                        "cong_level": busy_level
                    })

            context = {"buildings_info": selected_names_cong_levels,
                        "day_of_week": flask.request.form["day"],
                        "time_period": flask.request.form["time"]}
            return flask.render_template("predict.html", **context)
        else:
            return flask.render_template("error.html")
