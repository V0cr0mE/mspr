import dash
from dash import dcc, html, Input, Output, no_update,State
import pandas as pd
import plotly.express as px
import requests
import base64
from etl.etl_generique import detect_and_process
import base64
from werkzeug.utils import secure_filename
import os
from load.continent import insert_continents
from load.country import insert_countries
from load.pandemic import insert_pandemics
from load.daily_pandemic_country import insert_daily_pandemic_country_data
from load.pandemic_country import insert_pandemic_country_data
from models.config_db import connect_to_db

def init_dashboard(server):
    dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')
    UPLOAD_FOLDER = "C:/Users/Anes/MSPR/donnes"

    dash_app.layout = html.Div([
        # Navigation
        html.Nav([
            html.H2("Pandemic Statistics Dashboard", style={'color': 'white', 'margin': '0', 'padding': '10px', 'textAlign': 'center'}),
        ], style={'backgroundColor': 'rgba(0, 0, 0, 0)', 'padding': '10px'}),

        # Formulaire d'upload de fichiers
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
                    'height': '50px',
                    'lineHeight': '50px',
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
        html.Div([
            html.Button("Load", id='btn-load-all-db', n_clicks=0, style={
               'margin': '20px auto',
               'display': 'block',
               'backgroundColor': '#3498db',
               'color': 'white',
               'padding': '10px 20px',
               'borderRadius': '8px',
               'border': 'none',
               'fontWeight': 'bold',
               'cursor': 'pointer'}),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        html.Div(id='load-all-status', style={'color': 'white', 'textAlign': 'center','backgroundColor': 'rgba(255, 255, 255, 0.1)'}),

        # Dropdown pour sélectionner le pays et la pandémie
        html.Div([
            html.Div([
                html.Label("Select Country", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.Dropdown(id='country-dropdown', options=[], value=3,
                             style={'width': '100%', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '8px', 'border': '1px solid #ddd'}),
            ], style={'width': '15%', 'padding': '10px'}),
            html.Div([
                html.Label("Select Pandemic", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.Dropdown(id='pandemic-dropdown', options=[], value=1,
                             style={'width': '100%', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '8px', 'border': '1px solid #ddd'}),
            ], style={'width': '15%', 'padding': '10px'}),
            html.Div([
                html.Label("Type of statistic", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.Dropdown(
                    id='stat-type-dropdown',
                    options=[
                        {'label': 'Deaths', 'value': 'daily_new_deaths'},
                        {'label': 'Cases', 'value': 'daily_new_cases'},
                       
                    ],
                    value='daily_new_cases',
                    style={
                       'width': '100%',
                       'fontFamily': 'Arial, sans-serif',
                       'borderRadius': '8px',
                       'border': '1px solid #ddd'
                    }
                ),
            ], style={'width': '15%', 'padding': '10px'}),

            
            
            html.Div([
                html.Label("Select Date Range", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'}),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date="2020-01-01",
                    end_date="2025-01-01",
                    display_format='YYYY-MM-DD',
                    style={
                        'width': '100%',
                        'fontFamily': 'Arial, sans-serif',
                        'border': '1px solid #ddd',
                        'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.12)',
                        'fontSize': '5px',
                        'display': 'flex',
                        'justifyContent': 'space-between',
                    },
                ),
            ]),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '10px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}),

        # Graphiques
        html.Div(id='cards-container', style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center', 'margin': '20px auto'}),
        html.Div([
            html.Div([
                    dcc.Graph(id='continent-pie-chart', style={'width': '50%', 'display': 'inline-block'}),
                    dcc.Graph(id='recovery-trend', style={'width': '50%', 'display': 'inline-block'})
            ], style={'display': 'flex', 'width': '100%'}),
            html.Div([
               dcc.Graph(id='histogram', style={'width': '50%','display': 'inline-block'}),
               dcc.Graph(id='continent-bar-chart', style={'width': '50%','display': 'inline-block'}),
            ], style={'display': 'flex', 'width': '100%'}),
        ])
        

    ], style={
        'backgroundImage': 'url(https://mediclinic.scene7.com/is/image/mediclinic/hirslanden-corona-virus-teaser:1-1?_ck=1616227095797&wid=1050&hei=1050&dpr=off)',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'minHeight': '200vh',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': 'rgba(0, 0, 0, 0)'
    })
    
    @dash_app.callback(
      Output('upload-status', 'children'),
      Input('upload-file', 'contents'),
      Input('upload-file', 'filename'),
      prevent_initial_call=True
    )
    def handle_upload(contents, filename):
       if contents is None or filename is None:
          return "Aucun fichier sélectionné."

       try:
             # Décodage base64
             content_type, content_string = contents.split(',')
             decoded = base64.b64decode(content_string)

             # Enregistrement temporaire
             filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
             with open(filepath, "wb") as f:
                f.write(decoded)

             # Traitement automatique avec l'ETL générique
             detect_and_process(filepath)

             return f"fichier '{filename}' chargé et traité avec succès."

       except Exception as e:
         return f"Erreur lors du traitement du fichier : {e}"
     
    def charger_toutes_les_tables():
      try:
          conn = connect_to_db()

          base_path = "C:/Users/Anes/MSPR/donnes_clean/"

          insert_continents(conn, f"{base_path}worldometer_coronavirus_summary_data_clean.csv")
          insert_countries(conn, f"{base_path}worldometer_coronavirus_summary_data_clean.csv")
          insert_pandemics(conn)
          insert_daily_pandemic_country_data(conn, f"{base_path}worldometer_coronavirus_daily_data_clean.csv",1)
          insert_daily_pandemic_country_data(conn, f"{base_path}worldometer_coronavirus_daily_data_clean.csv",2)
          insert_pandemic_country_data(conn, f"{base_path}worldometer_coronavirus_summary_data_clean.csv")

          conn.close()
          return "Toutes les données ont été insérées dans la base avec succès !"

      except Exception as e:
        return f"Erreur lors de l'insertion : {str(e)}"
    
    
    @dash_app.callback(
      Output('load-all-status', 'children'),
      Input('btn-load-all-db', 'n_clicks'),
      prevent_initial_call=True
    )
    def handle_load_all(n_clicks):
      if n_clicks:
          return charger_toutes_les_tables()
      return dash.no_update

    def get_countries():
        response = requests.get('http://127.0.0.1:5000/country')
        return response.json() if response.status_code == 200 else []
       

    # def get_continents():
    #     response = requests.get('http://127.0.0.1:5000/continent')
    #     return response.json() if response.status_code == 200 else []
    
    def get_pandemics():
        response = requests.get('http://127.0.0.1:5000/pandemic')
        return response.json() if response.status_code == 200 else []

    def get_daily_pandemic(id_country, id_pandemic):
        response = requests.get(f'http://127.0.0.1:5000/daily_pandemic_country/{id_country}/{id_pandemic}')
        return response.json() if response.status_code == 200 else []

    def get_pandemic_by_continent():
        response = requests.get(f'http://127.0.0.1:5000/pandemic_country/continent')
        return response.json() if response.status_code == 200 else []

    # Callbacks pour les Dropdowns
    @dash_app.callback(
        Output('country-dropdown', 'options'),
        Input('country-dropdown', 'value')
    )
    def update_country_dropdown(value):
        countries = get_countries()
        return [{'label': country[1], 'value': country[0]} for country in countries]
       # Callbacks pour les Dropdowns
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
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_cards(country_id, pandemic_id,start_date,end_date):
        if not country_id or not pandemic_id:
            return html.P("Veuillez sélectionner un pays et une pandémie.", style={'textAlign': 'center', 'color': 'white'})

        response = requests.get(f'http://127.0.0.1:5000/pandemic_country/{country_id}/{pandemic_id}')
        if response.status_code == 200:
            data = response.json()
     
           
            total_deaths = data.get('total_deaths', 0)
            total_confirmed = data.get('total_confirmed', 0)
            population = data.get('population', 0)

            mortality_rate = (total_deaths / total_confirmed * 100) if total_confirmed else 0

            
            daily_data = get_daily_pandemic(country_id, pandemic_id)
            if daily_data:
               df_daily = pd.DataFrame(daily_data)
               df_daily['date'] = pd.to_datetime(df_daily['date'])
               df_filtered = df_daily[(df_daily['date'] >= start_date) & (df_daily['date'] <= end_date)]
               incidence = df_filtered['daily_new_cases'].sum()
               prevalence = df_filtered['active_cases'].mean()
               transmission_rate = (incidence / prevalence * 100)
            else:
              transmission_rate = 0
            print(incidence)
            print(prevalence)
            cards = [
                html.Div([html.H3("Total Deaths"), html.P(f"{data.get('total_deaths', 0)}")],
                         style={'border': '1px solid #d04e47', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#e67e22', 'font-weight': 'bold', 'font-size': '20px'}),
                html.Div([html.H3("Total Cases"), html.P(f"{data.get('total_confirmed', 0)}")],
                         style={'border': '1px solid #e67e22', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#5b8fd4', 'font-weight': 'bold', 'font-size': '20px'}),
                html.Div([html.H3("Total Recovered"), html.P(f"{data.get('total_recovered', 0)}")],
                         style={'border': '1px solid #2ecc71', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#27ae60', 'font-size': '20px', 'font-weight': 'bold'}),
                html.Div([html.H3("Transmission Rate"), html.P(f"{transmission_rate:.2f}%")],
                     style={'border': '1px solid #3498db', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)',
                            'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#3498db',
                            'font-size': '20px', 'font-weight': 'bold'}),
                html.Div([html.H3("Mortality Rate"), html.P(f"{mortality_rate:.2f}%")],
                     style={'border': '1px solid #c0392b', 'padding': '10px', 'width': '200px', 'backgroundColor': 'rgba(0, 0, 0, 0)',
                            'backdrop-filter': 'blur(50px)', 'borderRadius': '10px', 'textAlign': 'center', 'color': '#c0392b',
                            'font-size': '20px', 'font-weight': 'bold'})
            ]
            return cards
        return html.P("Données non trouvées.", style={'textAlign': 'center', 'color': 'black'})

    @dash_app.callback(
        Output('recovery-trend', 'figure'),
        [Input('country-dropdown', 'value'),
         Input('pandemic-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('stat-type-dropdown', 'value')]
    )
    def update_recovery_graph(country_id, pandemic_id, start_date, end_date,stat_type):
        if not country_id or not pandemic_id or not stat_type:
            return px.line(title="Sélectionnez un pays et une pandémie")

        data = get_daily_pandemic(country_id, pandemic_id)
        if not data:
            return px.line(title="Aucune donnée disponible")

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])

        df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        if stat_type not in df_filtered.columns:
            return px.line(title="Données manquantes {stat_type}")

        fig = px.line(df_filtered, x='date', y=stat_type,
                      title=f"Évolution de {stat_type.replace('_', ' ').capitalize()}",
                      labels={stat_type: stat_type.replace('_', ' ').capitalize(), 'date': 'Date'},
                      markers=True)

        fig.update_traces(line=dict(color='blue', width=2), marker=dict(size=6, color='red'))
        fig.update_layout(
            plot_bgcolor='blue',  
            paper_bgcolor='blue',  
            font=dict(color='white'),
            xaxis=dict(gridcolor='gray', color='white'),
            yaxis=dict(gridcolor='gray', color='white')
        )
        return fig

    @dash_app.callback(
        Output('continent-pie-chart', 'figure'),
        [Input('stat-type-dropdown', 'value')]
    )
    def update_continent_pie_chart(stat_type):
        continents = get_pandemic_by_continent()

        if not continents:
            return px.pie(title="Aucune donnée disponible")
        if stat_type == 'daily_new_cases':
            value_key = 'total_confirmed'
            title = "Répartition des Cas Confirmés par Continent"
        elif stat_type == 'daily_new_deaths':
            value_key = 'total_deaths'
            title = "Répartition des Décès par Continent"
        else:
            value_key = 'total_confirmed'
            title = "Répartition par Continent"

        continent_names = [continent['continent'] for continent in continents]
        values = [continent.get(value_key, 0) for continent in continents]

        fig = px.pie(
            names=continent_names,
            values=values,
            title=title
        )

        fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        fig.update_layout(
            plot_bgcolor='blue',
            paper_bgcolor='blue',
            font=dict(color='white')
        )
        return fig
    @dash_app.callback(
        Output('histogram', 'figure'),
        [Input('country-dropdown', 'value'),
         Input('pandemic-dropdown', 'value'),
         Input('stat-type-dropdown', 'value')]
    )
    def update_histogram(country_id, pandemic_id,stat_type):
        if not country_id or not pandemic_id or not stat_type:
            return px.histogram()
        
        data = get_daily_pandemic(country_id, pandemic_id)
        df = pd.DataFrame(data)
        
        if df.empty:
            return px.histogram()
        
        fig = px.histogram(df, x='date', y=stat_type, title='Histogramme des cas quotidiens', nbins=30
        )
        fig.update_traces(marker=dict(color='red'))
        fig.update_layout(
            plot_bgcolor='blue',
            paper_bgcolor='blue',
            font=dict(color='white')
        )
        return fig 
    
    @dash_app.callback(
        Output('continent-bar-chart', 'figure'),
       [Input('stat-type-dropdown', 'value')]
    )
    def update_continent_bar_chart(stat_type):
        data = get_pandemic_by_continent()

        if not data:
           return px.bar(title="Aucune donnée disponible")
         

        df = pd.DataFrame(data)
        if stat_type == 'daily_new_cases':
            y_column = 'total_confirmed'
            title = "Total Confirmed Cases par Continent"
        elif stat_type == 'daily_new_deaths':
            y_column = 'total_deaths'
            title = "Total Deaths par Continent"
        else:
            return px.bar(title="Statistique non reconnue")
        
        df[y_column] = pd.to_numeric(df[y_column], errors='coerce')

    
        df = df.sort_values(by=y_column, ascending=False)
        df['continent'] = pd.Categorical(df['continent'], categories=df['continent'].tolist(), ordered=True)

        fig = px.bar(df,
                   x='continent',
                   y=y_column,
                   color='continent',
                   title=title,
                   labels={'continent': 'Continent', y_column:'Valeur'})

        fig.update_layout(
          plot_bgcolor='blue',
          paper_bgcolor='blue',
          font=dict(color='white'),
          xaxis=dict(color='white'),
          yaxis=dict(color='white')
        )

        return fig


    return dash_app



