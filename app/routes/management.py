# Importing packages and modules
from flask import (
    render_template, 
    session,
    redirect,
    url_for,
    request,
    jsonify,
    Blueprint
)
from dao.db_access import DBAccess

# Setting the blueprint
management_bp = Blueprint("routes_management", __name__)

# Endpoint - Rendering management page
@management_bp.route("/management")
def management():
    if "active_user" not in session or session["active_user"] == None:
        return redirect(url_for("routes_login.login"))
    elif session["admin_access"]:
        db_access = DBAccess()
        users = db_access.get_users_management()
        matches = db_access.get_matches()
        return render_template("management.html", 
                               users=users,
                               matches=matches)

# Adding a new user
@management_bp.route("/adduser", methods=["POST",])
def add_user():
    try:
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        db_access = DBAccess()
        db_access.add_user(name, username, password)
        message = "Usuário adicionado com sucesso!"
        status_code = 200
    except:
        message = "Não foi possível adicionar o usuário!"
        status_code = 400
    return jsonify({"message" : message}), status_code

# Deleting a user
@management_bp.route("/deleteuser", methods=["POST",])
def delete_user():
    try:
        username = request.form["username"]
        db_access = DBAccess()
        db_access.delete_user(username)
        message = "Usuário removido com sucesso!"
        status_code = 200
    except:
        message = "Não foi possível remover o usuário!"
        status_code = 400
    return jsonify({"message" : message}), status_code

# Updating a user
@management_bp.route("/updateuser", methods=["POST",])
def update_user():
    try:
        print("a")
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        db_access = DBAccess()
        db_access.update_user(name, username, password)
        message = "Usuário removido com sucesso!"
        status_code = 200
    except:
        message = "Não foi possível remover o usuário!"
        status_code = 400
    return jsonify({"message" : message}), status_code

# Updating a match result
@management_bp.route("/updatematch", methods=["POST",])
def update_match():
    try:
        match_id = int(request.form["match_id"])
        if request.form["goals_1"] != "":
            goals_1 = int(request.form["goals_1"])
        else:
            goals_1 = None
        if request.form["goals_2"] != "":
            goals_2 = int(request.form["goals_2"])
        else:
            goals_2 = None
        if (goals_1 is None or goals_2 is None) and goals_1 != goals_2:
            raise Exception("Detectada combinação de gols inválida")
        else:
            db_access = DBAccess()
            db_access.update_match(match_id, goals_1, goals_2)
            db_access.update_scores(match_id, goals_1, goals_2)
            db_access.sum_scores()
            message = "Usuário removido com sucesso!"
            status_code = 200
    except:
        message = "Não foi possível remover o usuário!"
        status_code = 400
    return jsonify({"message" : message}), status_code