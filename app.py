import os
import sys
import requests
import dash
import pandas as pd
import plotly.express as px
from flask import Flask
from dash import dcc, html
from dash.dependencies import Input, Output
from routes.continent import bp as continent_bp
from routes.country import bp as country_bp
from routes.pandemic import bp as pandemic_bp
from routes.pandemic_country import bp as pandemic_country_bp
from routes.daily_pandemic_country import bp as daily_pandemic_country_bp


sys.path.append(os.path.join(os.path.dirname(__file__), 'load'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))


def create_app():
    app = Flask(__name__)


    app.register_blueprint(continent_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(pandemic_bp)
    app.register_blueprint(pandemic_country_bp)
    app.register_blueprint(daily_pandemic_country_bp)

    
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/')

    dash_app.layout = html.Div([
        html.H1("Statistiques Pandemic", style={'textAlign': 'center', 'color': 'black'}),

        
        dcc.Dropdown(id='country-dropdown', options=[], value=None, style={'width': '50%', 'margin': '20px auto'}),
        dcc.Dropdown(id='pandemic-dropdown', options=[], value=None, style={'width': '50%', 'margin': '20px auto'}),

        dcc.DatePickerRange(
            id='date-picker-range',
            start_date="2020-01-01",
            end_date="2025-01-01",   
            display_format='YYYY-MM-DD',
            style={'width': '50%', 'margin': '20px auto'}
        ),

        # Conteneur des cartes
        html.Div(id='cards-container', style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap', 'gap': '20px'}),

        # Graphique d'évolution des guérisons
        dcc.Graph(id='recovery-trend', style={'width': '80%', 'margin': '20px auto'})
    ], style={'backgroundColor': '#f0f0f0', 'minHeight': '100vh'})


    def get_countries():
        response = requests.get('http://127.0.0.1:5000/country')
        return response.json() if response.status_code == 200 else []

    def get_pandemics():
        response = requests.get('http://127.0.0.1:5000/pandemic')
        return response.json() if response.status_code == 200 else []

    def get_daily_pandemic(id_country, id_pandemic):
        response = requests.get(f'http://127.0.0.1:5000/daily_pandemic_country/{id_country}/{id_pandemic}')
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
            return html.P("Veuillez sélectionner un pays et une pandémie.", style={'textAlign': 'center', 'color': 'black'})

        response = requests.get(f'http://127.0.0.1:5000/pandemic_country/{country_id}/{pandemic_id}')
        if response.status_code == 200:
            data = response.json()
            cards = [
                html.Div([html.H3("Total Deaths"), html.P(f"{data.get('total_deaths', 0)}")],
                         style={'border': '1px solid #d04e47', 'padding': '10px', 'width': '200px', 'backgroundColor': '#b94a3b', 'borderRadius': '10px', 'textAlign': 'center', 'color': 'white'}),
                html.Div([html.H3("Total Confirmed Cases"), html.P(f"{data.get('total_confirmed', 0)}")],
                         style={'border': '1px solid #e67e22', 'padding': '10px', 'width': '200px', 'backgroundColor': '#e17e22', 'borderRadius': '10px', 'textAlign': 'center', 'color': 'white'}),
                html.Div([html.H3("Total Recovered"), html.P(f"{data.get('total_recovered', 0)}")],
                         style={'border': '1px solid #2ecc71', 'padding': '10px', 'width': '200px', 'backgroundColor': '#229f59', 'borderRadius': '10px', 'textAlign': 'center', 'color': 'white'})
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
        return fig

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
