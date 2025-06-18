import os
import sys
import requests
from flask import Flask, send_from_directory
from flask_cors import CORS 
from flasgger import Swagger

# Suppression des imports liés à Dash
# import base64
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html
# from dash.dependencies import Input, Output

# Ajout du dossier des blueprints
sys.path.append(os.path.join(os.path.dirname(__file__), 'load'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

from routes.continent import bp as continent_bp
from routes.country import bp as country_bp
from routes.pandemic import bp as pandemic_bp
from routes.pandemic_country import bp as pandemic_country_bp
from routes.daily_pandemic_country import bp as daily_pandemic_country_bp
from routes.prediction import bp as prediction_bp

UPLOAD_FOLDER = 'donnes'
# Path to the cleaned data directory inside the backend folder
CLEAN_DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'donnes_clean')
ALLOWED_EXTENSIONS = {'csv', 'txt', 'pdf'}

def allowed_file(filename):
    return (
        '.' in filename 
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def create_app():
    # On précise que le dossier statique (React build) se trouve dans "dashboard/dist"
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), 'dashboard', 'dist'),
        static_url_path=''
    )
    CORS(app)
    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Pandemic API",
            "description": "API pour gérer les données de pandémie",
            "version": "1.0"
        }
    })

    app.config['SECRET_KEY'] = 'votre_clé_secrète'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Création des dossiers si nécessaire
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    os.makedirs(CLEAN_DATA_FOLDER, exist_ok=True)

    # Enregistrement des blueprints
    app.register_blueprint(continent_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(pandemic_bp)
    app.register_blueprint(pandemic_country_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(daily_pandemic_country_bp)

    # Route générique pour servir l’application React
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        """
        Sert le fichier index.html de la build React pour toutes les routes
        non gérées par l’API, et renvoie les fichiers statiques (JS/CSS) si on
        les demande explicitement.
        """
        # Chemin complet vers le dossier dist
        static_dir = app.static_folder

        if path != "" and os.path.exists(os.path.join(static_dir, path)):
            # Si le fichier demandé existe dans dist (ex. main.js, style.css, etc.), on le renvoie
            return send_from_directory(static_dir, path)
        else:
            # Sinon, on renvoie systématiquement index.html
            return send_from_directory(static_dir, 'index.html')

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
