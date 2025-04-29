# Dans app.py

from flask import Flask
from routes.continent import bp as continent_bp
from routes.country import bp as country_bp
from routes.pandemic import bp as pandemic_bp
from routes.pandemic_country import bp as pandemic_country_bp
from routes.daily_pandemic_country import bp as daily_pandemic_country_bp
from config.dash_app import create_dash_app
from config.config import UPLOAD_FOLDER, CLEAN_DATA_FOLDER
from config.file_handler import save_uploaded_file
import os

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "votre_clé_secrète"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    os.makedirs(CLEAN_DATA_FOLDER, exist_ok=True)

    app.register_blueprint(continent_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(pandemic_bp)
    app.register_blueprint(pandemic_country_bp)
    app.register_blueprint(daily_pandemic_country_bp)

    # Ajoute Dash à l'application Flask
    create_dash_app(app)  # Crée l'interface Dash et l'ajoute à l'app Flask

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)