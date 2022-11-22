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
guesses_bp = Blueprint("routes_guesses", __name__)

# Endpoint - Rendering the guess page
@guesses_bp.route("/guesses")
def guesses():
    if "active_user" not in session or session["active_user"] == None:
        return redirect(url_for("routes_login.login"))
    else:
        db_access = DBAccess()
        matches = db_access.get_matches()
        guesses, score = db_access.get_guesses(session["active_user"])
        return render_template("guesses.html", 
                               matches=matches,
                               guesses=guesses,
                               score=score,
                               username=session["active_user"],
                               admin_access=session["admin_access"])

# Saving guesses of a user
@guesses_bp.route("/saveguess", methods=["POST",])
def save_guesses():
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
        db_access = DBAccess()
        db_access.save_guess(session["active_user"], match_id, goals_1, goals_2)
        message = "Usuário removido com sucesso!"
        status_code = 200
    except:
        message = "Não foi possível remover o usuário!"
        status_code = 400
    return jsonify({"message" : message}), status_code

# Showing result comparison along all users
@guesses_bp.route("/getcomparison", methods=["POST",])
def get_comparison():
    try:
        match_id = request.form["match_id"]
        db_access = DBAccess()
        comparison = db_access.get_comparison(match_id)
        status_code = 200
    except:
        comparison = "Não foi possível obter comparações!"
        status_code = 400
    return jsonify({"comparison" : comparison}), status_code