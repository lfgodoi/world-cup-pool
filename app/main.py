# Importing packages and modules
from flask import (
    Flask, 
    render_template, 
    session,
    redirect,
    url_for,
    request
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
        guesses = db_access.get_guesses()
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
        return render_template("management.html", 
                               users=users)

# Login page
@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

# Authentication
@app.route("/authenticate", methods=["POST",])
def authenticate():
    db_access = DBAccess()
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

# Running the app
if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=False)