import os
import sys
import requests
import dash
import base64
import pandas as pd
import plotly.express as px
from flask import Flask
from werkzeug.utils import secure_filename
from dash import dcc, html
from dash.dependencies import Input, Output
from routes.continent import bp as continent_bp
from routes.country import bp as country_bp
from routes.pandemic import bp as pandemic_bp
from routes.pandemic_country import bp as pandemic_country_bp
from routes.daily_pandemic_country import bp as daily_pandemic_country_bp
from etl.etl_generique import extract, transform, load  # Assurez-vous que ces fonctions soient accessibles

sys.path.append(os.path.join(os.path.dirname(__file__), 'load'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

# Configuration pour l'upload de fichiers
UPLOAD_FOLDER = 'donnes'  # Dossier où les fichiers seront stockés
CLEAN_DATA_FOLDER = 'C:/Users/Anes/MSPR/donnes_clean/'
ALLOWED_EXTENSIONS = {'csv', 'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'votre_clé_secrète'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Crée le dossier 'donnes' s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # Crée le dossier 'donnes_clean' s'il n'existe pas
    os.makedirs(CLEAN_DATA_FOLDER, exist_ok=True)

    # Enregistrement des blueprints
    app.register_blueprint(continent_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(pandemic_bp)
    app.register_blueprint(pandemic_country_bp)
    app.register_blueprint(daily_pandemic_country_bp)

    # Configuration de Dash
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/')

    # Layout de Dash
    dash_app.layout = html.Div([
        # Navigation
        html.Nav([
            html.H2("Pandemic Statistics Dashboard", style={'color': 'white', 'margin': '0', 'padding': '10px', 'textAlign': 'center'}),
        ], style={'backgroundColor': 'rgba(0, 0, 0, 0)', 'padding': '10px'}),

        html.Div([
            html.H3("Uploader un fichier", style={'color': 'white', 'textAlign': 'center'}),
            dcc.Upload(
                id='upload-file',
                children=html.Div([
                    'Glissez-déposez ou ',
                    html.A('sélectionnez un fichier')
                ]),
                style={
                    'width': '50%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px auto',
                    'color': 'white',
                    'backgroundColor': 'rgba(255, 255, 255, 0.1)',
                },
                multiple=False
            ),
            html.Div(id='upload-status', style={'textAlign': 'center', 'color': 'white'})
        ], style={'margin': '20px'}),
         
        # Dropdown pour sélectionner le pays, la pandémie et le continent
        html.Div([
            html.Div([
                html.Label("Select Country", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.Dropdown(id='country-dropdown', options=[], value=None,
                             style={'width': '100%', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '8px', 'border': '1px solid #ddd'}),
            ], style={'width': '15%', 'padding': '10px'}),
            html.Div([
                html.Label("Select Pandemic", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.Dropdown(id='pandemic-dropdown', options=[], value=None,
                             style={'width': '100%', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '8px', 'border': '1px solid #ddd'}),
            ], style={'width': '15%', 'padding': '10px'}),
            html.Div([
                html.Label("Select Continent", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.Dropdown(id='continent-dropdown', options=[], value=None,
                             style={'width': '100%', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '8px', 'border': '1px solid #ddd'}),
            ], style={'width': '15%', 'padding': '10px'}),
            html.Div([
                html.Label("Select Date Range", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date="2020-01-01",
                    end_date="2025-01-01",
                    display_format='YYYY-MM-DD',
                    style={'width': '100%', 'borderRadius': '8px'}

                )
            ], style={'width': '30%', 'padding': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '10px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}),

        # Graphiques
        html.Div(id='cards-container', style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center', 'margin': '20px auto'}),
        dcc.Graph(id='continent-pie-chart', style={'width': '50%', 'margin': '40px'}),
        dcc.Graph(id='recovery-trend', style={'width': '50%', 'margin': '40px', 'Color': 'black'})
    ], style={
        'backgroundImage': 'url(https://mediclinic.scene7.com/is/image/mediclinic/hirslanden-corona-virus-teaser:1-1?_ck=1616227095797&wid=1050&hei=1050&dpr=off)',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center center',
        'minHeight': '100vh',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': 'rgba(0, 0, 0, 0)'
    })

    # Callback pour gérer l'upload de fichiers
    @dash_app.callback(
        Output('upload-status', 'children'),
        Input('upload-file', 'contents'),
        Input('upload-file', 'filename'),
        prevent_initial_call=True
    )
    
    def handle_upload(contents, filename):
        if contents is None or filename is None:
            return "Aucun fichier sélectionné."

        # Décoder le fichier
        _, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # Sauvegarder le fichier dans le dossier 'donnes'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)) 
        with open(filepath, 'wb') as f:
            f.write(decoded)

        file_type_map = {
            "worldometer_coronavirus_daily_data.csv": "worldometer_daily",
            "worldometer_coronavirus_summary_data.csv": "worldometer_summary",
            "owid-monkeypox-data.csv": "monkeypox"
        }
        
        file_type = file_type_map.get(filename)

        if file_type is None:
            return "Type de fichier non reconnu. Veuillez télécharger un fichier valide."

        # Appel de la logique ETL pour transformer les données
        raw_data = extract(filepath)
        if raw_data is not None:
            cleaned_data = transform(raw_data, file_type)

            # Spécifiez le chemin et le nom du fichier de sortie
            output_file = os.path.join(CLEAN_DATA_FOLDER, f"{filename.replace('.csv', '_clean.csv')}")
            load(cleaned_data, output_file)  

            return f"Fichier '{filename}' uploadé avec succès et transformé dans '{output_file}' !"
        else:
            return "Erreur lors de l'extraction des données."

    # Fonctions pour récupérer les données
    def get_countries():
        response = requests.get('http://127.0.0.1:5000/country')
        return response.json() if response.status_code == 200 else []

    def get_continents():
        response = requests.get('http://127.0.0.1:5000/continent')
        return response.json() if response.status_code == 200 else []

    def get_pandemics():
        response = requests.get('http://127.0.0.1:5000/pandemic')
        return response.json() if response.status_code == 200 else []

    def get_daily_pandemic(id_country, id_pandemic):
        response = requests.get(f'http://127.0.0.1:5000/daily_pandemic_country/{id_country}/{id_pandemic}')
        return response.json() if response.status_code == 200 else []

    def get_pandemic_by_continent():
        response = requests.get('http://127.0.0.1:5000/pandemic_country/continent')
        return response.json() if response.status_code == 200 else []

    # Callbacks pour les Dropdowns
    @dash_app.callback(
        Output('country-dropdown', 'options'),
        Input('country-dropdown', 'value')
    )
    def update_country_dropdown(value):
        countries = get_countries()
        return [{'label': country[1], 'value': country[0]} for country in countries]

    @dash_app.callback(
        Output('continent-dropdown', 'options'),
        Input('continent-dropdown', 'value')
    )
    def update_continent_dropdown(value):
        continents = get_continents()
        return [{'label': continent['continent'], 'value': continent['id']} for continent in continents]

    @dash_app.callback(
        Output('pandemic-dropdown', 'options'),
        Input('pandemic-dropdown', 'value')
    )
    def update_pandemic_dropdown(value):
        pandemics = get_pandemics()
        return [{'label': pandemic['name'], 'value': pandemic['id_pandemic']} for pandemic in pandemics]

    @dash_app.callback(
        Output('cards-container', 'children'),
        [Input('country-dropdown', 'value'),
         Input('pandemic-dropdown', 'value'),
         Input('continent-dropdown', 'value')]
    )
    def update_cards(country_id, pandemic_id, continent_id):
        if not country_id or not pandemic_id:
            return html.P("Veuillez sélectionner un pays et une pandémie.", style={'textAlign': 'center', 'color': 'white'})

        response = requests.get(f'http://127.0.0.1:5000/pandemic_country/{country_id}/{pandemic_id}')
        if response.status_code == 200:
            data = response.json()
            cards = [
                html.Div([html.H3("Total Deaths"), html.P(f"{data.get('total_deaths', 0)}")],
                         style={'border': '1px solid #d04e47', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#e67e22', 'font-weight': 'bold', 'font-size': '20px'}),
                html.Div([html.H3("Total Cases"), html.P(f"{data.get('total_confirmed', 0)}")],
                         style={'border': '1px solid #e67e22', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#5b8fd4', 'font-weight': 'bold', 'font-size': '20px'}),
                html.Div([html.H3("Total Recovered"), html.P(f"{data.get('total_recovered', 0)}")],
                         style={'border': '1px solid #2ecc71', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#27ae60', 'font-size': '20px', 'font-weight': 'bold'})
            ]
            return cards
        return html.P("Données non trouvées.", style={'textAlign': 'center', 'color': 'black'})

    @dash_app.callback(
        Output('recovery-trend', 'figure'),
        [Input('country-dropdown', 'value'),
         Input('pandemic-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_recovery_graph(country_id, pandemic_id, start_date, end_date):
        if not country_id or not pandemic_id:
            return px.line(title="Sélectionnez un pays et une pandémie")

        data = get_daily_pandemic(country_id, pandemic_id)
        if not data:
            return px.line(title="Aucune donnée disponible")

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])

        df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        if 'daily_new_cases' not in df_filtered.columns:
            return px.line(title="Données manquantes")

        fig = px.line(df_filtered, x='date', y='daily_new_cases',
                      title="Évolution du Nombre de Cas Quotidiens",
                      labels={'daily_new_cases': 'Cas quotidiens', 'date': 'Date'},
                      markers=True)

        fig.update_traces(line=dict(color='blue', width=2), marker=dict(size=6, color='red'))
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Couleur du fond du graphique
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Couleur de fond du cadre
            font=dict(color='white'),
            xaxis=dict(gridcolor='gray', color='white'),
            yaxis=dict(gridcolor='gray', color='white')
        )
        return fig

    @dash_app.callback(
        Output('continent-pie-chart', 'figure'),
        [Input('continent-dropdown', 'value')]
    )
    def update_continent_pie_chart(continent_id):
        continents = get_pandemic_by_continent()

        if not continents:
            return px.pie(title="Aucune donnée disponible")

        continent_names = [continent['continent'] for continent in continents]
        continent_cases = [continent.get('cases', 0) for continent in continents]

        fig = px.pie(
            names=continent_names,
            values=continent_cases,
            title="Répartition des Cas par Continent"
        )

        fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        fig.update_layout(
            plot_bgcolor='blue',
            paper_bgcolor='blue',
            font=dict(color='white')
        )
        return fig

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()