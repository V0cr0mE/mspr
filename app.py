import os
import sys
import requests
import dash
import base64
import pandas as pd
import plotly.express as px
from flask import Flask
from flask_cors import CORS 
from flasgger import Swagger
from werkzeug.utils import secure_filename
from dash import dcc, html
from dash.dependencies import Input, Output
from routes.continent import bp as continent_bp
from routes.country import bp as country_bp
from routes.pandemic import bp as pandemic_bp
from routes.pandemic_country import bp as pandemic_country_bp
from routes.daily_pandemic_country import bp as daily_pandemic_country_bp
from templates.dashboard import init_dashboard
sys.path.append(os.path.join(os.path.dirname(__file__), 'load'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

<<<<<<< HEAD
# Configuration pour l'upload de fichiers
UPLOAD_FOLDER = 'donnes'  
=======
from routes.prediction import bp as prediction_bp
UPLOAD_FOLDER = 'donnes'
>>>>>>> 84497e9cce70d33ec028c2e0e041b077d81c8ff2
CLEAN_DATA_FOLDER = '../donnes_clean/'
ALLOWED_EXTENSIONS = {'csv', 'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__) 
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

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    os.makedirs(CLEAN_DATA_FOLDER, exist_ok=True)

    app.register_blueprint(continent_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(pandemic_bp)
    app.register_blueprint(pandemic_country_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(daily_pandemic_country_bp)


    init_dashboard(app)

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
