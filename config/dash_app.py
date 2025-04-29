# Dans dash_app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from config.file_handler import save_uploaded_file
from etl.etl_generique import extract, transform, load
from config.config import CLEAN_DATA_FOLDER
import os

def create_dash_app(server):
    dash_app = dash.Dash(__name__, server=server, url_base_pathname="/")

    dash_app.layout = html.Div([
        html.H2("Pandemic Dashboard", style={"textAlign": "center", "color": "white"}),
        
        # Composant Upload de fichier
        dcc.Upload(
            id="upload-file",
            children=html.Div(["Glissez-déposez ou ", html.A("sélectionnez un fichier")]),
            multiple=False,
            style={'textAlign': 'center', 'color': 'white', 'border': '1px dashed #fff', 'padding': '10px', 'borderRadius': '10px', 'cursor': 'pointer'}
        ),
        
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
        
        # Sauvegarde du fichier
        filepath = save_uploaded_file(contents, filename)
        
        # Logique ETL (Extraction, Transformation, Chargement)
        raw_data = extract(filepath)
        if raw_data is not None:
            cleaned_data = transform(raw_data, "generic")
            output_file = os.path.join(CLEAN_DATA_FOLDER, f"{filename.replace('.csv', '_clean.csv')}")
            load(cleaned_data, output_file)
            return f"Fichier {filename} transformé et sauvegardé !"
        else:
            return "Erreur lors de l'extraction des données."
    
    return dash_app

    @app.callback(
    Output('graph-container', 'children'),
    [Input('some-dropdown', 'value')]
    )
    
    def update_graph(selected_value):
        # Récupérer les données en fonction de la sélection
        data = fetch_data_based_on_input(selected_value)  # Remplace cette fonction par ton propre appel API ou fonction

        # Création du graphique
        fig = px.line(data, x='date', y='cases', title="Evolution des cas")
        return dcc.Graph(figure=fig)
