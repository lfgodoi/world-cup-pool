# Importing packages and modules
from flask import (
    render_template, 
    session,
    redirect,
    url_for,
    Blueprint
)
from dao.db_access import DBAccess

# Setting the blueprint
ranking_bp = Blueprint("routes_ranking", __name__)

# Endpoint - Rendering ranking page
@ranking_bp.route("/ranking")
def ranking():
    if "active_user" not in session or session["active_user"] == None:
        return redirect(url_for("routes_login.login"))
    else:
        db_access = DBAccess()
        users = db_access.get_users_ranking()
        return render_template("ranking.html", 
                               users=users,
                               admin_access=session["admin_access"])