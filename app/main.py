# Importing packages and modules
from flask import Flask
import json
import os
from routes.login import login_bp
from routes.guesses import guesses_bp
from routes.ranking import ranking_bp
from routes.rules import rules_bp
from routes.management import management_bp

# Reading the config file
with open("./dao/config.json", "rb") as file:
    config = json.load(file)

# Instantiating the app
app = Flask(__name__, template_folder="./templates", static_folder="static")
app.config['SECRET_KEY'] = 'mYkEy'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Registering every route
app.register_blueprint(login_bp)
app.register_blueprint(guesses_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(rules_bp)
app.register_blueprint(management_bp)

# Running the app
if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=True)