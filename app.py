import os
import sys
from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
from routes.continent import bp as continent_bp
from routes.country import bp as country_bp
from routes.pandemic import bp as pandemic_bp
from routes.pandemic_country import bp as pandemic_country_bp
from routes.daily_pandemic_country import bp as daily_pandemic_country_bp


# Ajouter les dossiers 'load' et 'etl' au chemin d'importation
sys.path.append(os.path.join(os.path.dirname(__file__), 'load'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

# Créer une instance de l'application Flask
def create_app():
    app = Flask(__name__)

    # Enregistrer les Blueprints (routes) pour chaque table
    app.register_blueprint(continent_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(pandemic_bp)
    app.register_blueprint(pandemic_country_bp)
    app.register_blueprint(daily_pandemic_country_bp)
    

   
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/')

    
    dash_app.layout = html.Div([
        html.H1("Statistiques Pandémies", style={'textAlign': 'center', 'color': 'black'}),
        dcc.Dropdown(id='country-dropdown', options=[], value=None, style={'width': '50%', 'margin': '20px auto'}),
        html.Br(),
        dcc.Dropdown(id='pandemic-dropdown', options=[], value=None, style={'width': '50%', 'margin': '20px auto'}),
        html.Div(id='cards-container', style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap', 'gap': '20px'}),
    ], style={'backgroundColor': '#f0f0f0', 'minHeight': '100vh'})  # Fond blanc cassé pour la plateforme

   
    def get_countries():
        response = requests.get('http://127.0.0.1:5000/country')  
        return response.json() if response.status_code == 200 else []

   
    def get_pandemics():
        response = requests.get('http://127.0.0.1:5000/pandemic')  
        return response.json() if response.status_code == 200 else []

    
    @dash_app.callback(
        Output('country-dropdown', 'options'),
        Input('country-dropdown', 'value')
    )
    def update_dropdown(value):
        countries = get_countries()
        return [{'label': country[1], 'value': country[0]} for country in countries]

 
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
         Input('pandemic-dropdown', 'value')]
    )
    def update_cards(country_id, pandemic_id):
        if not country_id or not pandemic_id:
            return html.P("Please select a country and a pandemic.", style={'textAlign': 'center', 'color': 'black'})
        
        response = requests.get(f'http://127.0.0.1:5000/pandemic_country/{country_id}/{pandemic_id}')
        if response.status_code == 200:
            data = response.json()
            cards = [
                html.Div([html.H3("Total Deaths"), html.P(f"{data.get('total_deaths', 0)}")],
                         style={'border': '1px solid #d04e47', 'padding': '10px', 'width': '200px', 'display': 'inline-block', 'backgroundColor': '#b94a3b', 'borderRadius': '10px', 'textAlign': 'center', 'color': 'white'}),
                html.Div([html.H3("Total Confirmed Cases"), html.P(f"{data.get('total_confirmed', 0)}")],
                         style={'border': '1px solid #e67e22', 'padding': '10px', 'width': '200px', 'display': 'inline-block', 'backgroundColor': '#e17e22', 'borderRadius': '10px', 'textAlign': 'center', 'color': 'white'}),
                html.Div([html.H3("Total Recovered"), html.P(f"{data.get('total_recovered', 0)}")],
                         style={'border': '1px solid #2ecc71', 'padding': '10px', 'width': '200px', 'display': 'inline-block', 'backgroundColor': '#229f59', 'borderRadius': '10px', 'textAlign': 'center', 'color': 'white'})
            ]
            return cards
        return html.P("Data not found for the selected country and pandemic.", style={'textAlign': 'center', 'color': 'black'})

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
