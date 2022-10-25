# Importing packages and modules
from flask import Flask, render_template
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
@app.route("/")
@app.route("/guesses")
def guesses():
    db_access = DBAccess()
    matches = db_access.get_matches()
    guesses = db_access.get_guesses()
    return render_template("guesses.html", 
                           matches=matches,
                           guesses=guesses)

# Endpoint - Rendering ranking page
@app.route("/ranking")
def ranking():
    db_access = DBAccess()
    users = db_access.get_users()
    return render_template("ranking.html", 
                           users=users)

# Running the app
if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=False)