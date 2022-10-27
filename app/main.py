# Importing packages and modules
from flask import (
    Flask, 
    render_template, 
    session,
    redirect,
    url_for,
    request,
    jsonify
)
import json
import os
from dao.db_access import DBAccess

# Reading the config file
with open("./dao/config.json", "rb") as file:
    config = json.load(file)

# Instantiating the app
app = Flask(__name__, template_folder="./templates", static_folder="static")
app.config['SECRET_KEY'] = 'mYkEy'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Endpoint - Rendering the guess page
@app.route("/guesses")
def guesses():
    if "active_user" not in session or session["active_user"] == None:
        return redirect(url_for("login"))
    else:
        db_access = DBAccess()
        matches = db_access.get_matches()
        guesses = db_access.get_guesses(session["active_user"])
        return render_template("guesses.html", 
                               matches=matches,
                               guesses=guesses,
                               admin_access=session["admin_access"])

# Endpoint - Rendering ranking page
@app.route("/ranking")
def ranking():
    if "active_user" not in session or session["active_user"] == None:
        return redirect(url_for("login"))
    else:
        db_access = DBAccess()
        users = db_access.get_users_ranking()
        return render_template("ranking.html", 
                               users=users,
                               admin_access=session["admin_access"])

# Endpoint - Rendering management page
@app.route("/management")
def management():
    if "active_user" not in session or session["active_user"] == None:
        return redirect(url_for("login"))
    elif session["admin_access"]:
        db_access = DBAccess()
        users = db_access.get_users_management()
        matches = db_access.get_matches()
        return render_template("management.html", 
                               users=users,
                               matches=matches)

# Login page
@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

# Authentication
@app.route("/authenticate", methods=["POST",])
def authenticate():
    db_access = DBAccess()
    print(request.form)
    user = db_access.get_user(request.form["username"])
    if request.form["password"] == user["password"]:
        session["active_user"] = user["username"]
        session["admin_access"] = user["admin_access"]
        return redirect(url_for("guesses"))
    else:
        return redirect(url_for("login"))

# Logout
@app.route("/logout")
def logout():
    session["active_user"] = None
    return redirect(url_for("routes_login.login"))

# Adding a new user
@app.route("/adduser", methods=["POST",])
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
@app.route("/deleteuser", methods=["POST",])
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
@app.route("/updateuser", methods=["POST",])
def update_user():
    try:
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

# Saving guesses of a user
@app.route("/saveguesses", methods=["POST",])
def save_guesses():
    try:
        guesses = request.get_json()["guesses"]
        db_access = DBAccess()
        db_access.save_guesses(session["active_user"], guesses)
        message = "Usuário removido com sucesso!"
        status_code = 200
    except:
        message = "Não foi possível remover o usuário!"
        status_code = 400
    return jsonify({"message" : message}), status_code

# Updating a match result
@app.route("/updatematch", methods=["POST",])
def update_match():
    try:
        match_id = int(request.form["match_id"])
        goals_1 = int(request.form["goals_1"])
        goals_2 = int(request.form["goals_2"])
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

# Running the app
if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=False)