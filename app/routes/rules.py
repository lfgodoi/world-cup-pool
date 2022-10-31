# Importing packages and modules
from flask import (
    render_template, 
    session,
    redirect,
    url_for,
    Blueprint
)

# Setting the blueprint
rules_bp = Blueprint("routes_rules", __name__)

# Endpoint - Rendering rules page
@rules_bp.route("/rules")
def rules():
    if "active_user" not in session or session["active_user"] == None:
        return redirect(url_for("routes_login.login"))
    else:
        return render_template("rules.html",
                               admin_access=session["admin_access"])