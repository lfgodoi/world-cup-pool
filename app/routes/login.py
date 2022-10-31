# Importing packages and modules
from flask import (
    render_template, 
    session,
    redirect,
    url_for,
    request,
    Blueprint
)
from dao.db_access import DBAccess

# Setting the blueprint
login_bp = Blueprint("routes_login", __name__)

# Login page
@login_bp.route("/")
@login_bp.route("/login")
def login():
    args = request.args.to_dict()
    if args == {}:
        login_error = False
    else:
        login_error = request.args["login_error"]
    return render_template("login.html",
                           login_error=login_error)

# Authentication
@login_bp.route("/authenticate", methods=["POST",])
def authenticate():
    db_access = DBAccess()
    user = db_access.get_user(request.form["username"])
    if user is not None:
        if request.form["password"] == user["password"]:
            session["active_user"] = user["username"]
            session["admin_access"] = user["admin_access"]
            return redirect(url_for("routes_guesses.guesses"))
        else:
            return redirect(url_for("routes_login.login", login_error=True))   
    else:
        return redirect(url_for("routes_login.login", login_error=True))

# Logout
@login_bp.route("/logout")
def logout():
    session["active_user"] = None
    return redirect(url_for("routes_login.login", login_error=False))
