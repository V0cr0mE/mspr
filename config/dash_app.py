import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from config.file_handler import save_uploaded_file
from etl.etl_generique import extract, transform, load
from config.config import CLEAN_DATA_FOLDER
import os
import pandas as pd
import plotly.express as px

def create_dash_app(server):
    dash_app = dash.Dash(__name__, server=server, url_base_pathname="/")
    dash_app.layout = html.Div([
        html.H2("Pandemic Dashboard", style={"textAlign": "center", "color": "white"}),
        dcc.Upload(id="upload-file", children=html.Div(["Glissez-déposez ou ", html.A("sélectionnez un fichier")]), multiple=False),
        html.Div(id="upload-status", style={"textAlign": "center", "color": "white"}),
    ])
    
    @dash_app.callback(
        Output("upload-status", "children"),
        [Input("upload-file", "contents"), Input("upload-file", "filename")],
        prevent_initial_call=True,
    )
    def handle_upload(contents, filename):
        if not contents or not filename:
            return "Aucun fichier sélectionné."
        
        filepath = save_uploaded_file(contents, filename)
        raw_data = extract(filepath)
        if raw_data is not None:
            cleaned_data = transform(raw_data, "generic")
            output_file = os.path.join(CLEAN_DATA_FOLDER, f"{filename.replace('.csv', '_clean.csv')}")
            load(cleaned_data, output_file)
            return f"Fichier {filename} transformé et sauvegardé !"
        else:
            return "Erreur lors de l'extraction des données."
    
    return dash_app
