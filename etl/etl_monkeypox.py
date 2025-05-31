import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from models.config_db import connect_to_db
from load.daily_pandemic_country import insert_daily_pandemic_country_data


<<<<<<< HEAD
# Extraction
=======
# --- Extraction ---
>>>>>>> 84497e9cce70d33ec028c2e0e041b077d81c8ff2
def extract(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur de chargement : {e}")
        return None

<<<<<<< HEAD

# Transformation
def transform(data):
    try:
        # Suppression de la colonne 'iso_code'
        if "iso_code" in data.columns:
            data = data.drop(columns=["iso_code"])

        # Renommer les colonnes
        data = data.rename(
            columns={
                "new_cases": "daily_new_cases",
                "new_deaths": "daily_new_deaths",
                "location": "country",
            }
        )

        # Filtrer les lignes où 'country' est l'une des valeurs suivantes : "Africa", "Europe", "North America", "South America", "Asia", "World"
        countries_to_remove = [
            "Africa",
            "Europe",
            "North America",
            "South America",
            "Asia",
            "World",
            "Puerto Rico",
        ]
        data = data[~data["country"].isin(countries_to_remove)]

        # Modifier les noms de pays : "United States" => "US" et "United Kingdom" => "UK"
        data["country"] = data["country"].replace(
            {"United States": "USA", "United Kingdom": "UK"}
        )

        # Remplacer les espaces par des underscores dans 'country'
        data["country"] = data["country"].str.replace(" ", "_")

        data["country"] = data["country"].str.replace(
            "Saint_Martin_(French_part)", "Saint_Martin"
        )
        data["country"] = data["country"].str.replace(
            "Democratic_Republic_of_Congo", "Democratic_Republic_Of_The_Congo"
        )
        data["country"] = data["country"].str.replace("Vietnam", "Viet_Nam")
        data["country"] = data["country"].str.replace(
            "Bosnia_and_Herzegovina", "Bosnia_And_Herzegovina"
        )
        data["country"] = data["country"].str.replace("Czechia", "Czech_Republic")

        # Remplacer les valeurs manquantes par 0 pour les colonnes numériques
        numeric_columns = [
            "total_cases",
            "total_deaths",
            "daily_new_cases",
            "daily_new_deaths",
            "new_cases_smoothed",
            "new_deaths_smoothed",
            "new_cases_per_million",
            "total_cases_per_million",
            "new_cases_smoothed_per_million",
            "new_deaths_per_million",
            "total_deaths_per_million",
            "new_deaths_smoothed_per_million",
        ]

        data[numeric_columns] = data[numeric_columns].fillna(0)

        # Conversion des valeurs numériques en int
        data[numeric_columns] = data[numeric_columns].astype("int64")
=======
# --- Transformation ---
def transform(data):
    try:
        # Suppression de colonnes inutiles
        cols_to_drop = ['iso_code']
        data.drop(columns=[col for col in cols_to_drop if col in data.columns], inplace=True)

        # Renommage des colonnes
        data.rename(columns={
            'new_cases': 'daily_new_cases',
            'new_deaths': 'daily_new_deaths',
            'location': 'country',
            'total_cases':'active_cases'
        }, inplace=True)

        # Suppression des continents et agrégats globaux
        countries_to_exclude = ["Africa", "Europe", "North America", "South America", "Asia", "World", "Puerto Rico","Oceania"]
        data = data[~data['country'].isin(countries_to_exclude)]

        # Uniformisation des noms de pays
        data['country'] = data['country'].replace({
            "United States": "USA",
            "United Kingdom": "UK",
            "Saint Martin (French part)": "Saint_Martin",
            "Democratic Republic of Congo": "Democratic_Republic_Of_The_Congo",
            "Vietnam": "Viet_Nam",
            "Bosnia and Herzegovina": "Bosnia_And_Herzegovina",
            "Czechia": "Czech_Republic"
        })
        data['country'] = data['country'].str.strip().str.replace(" ", "_")

        # Remplissage des valeurs manquantes par 0 pour les colonnes numériques
        numeric_columns = data.select_dtypes(include='number').columns
        data[numeric_columns] = data[numeric_columns].fillna(0)

        # Suppression des colonnes redondantes (dérivées ou inutiles)
        redundant_cols = [
            'new_cases_smoothed', 'new_deaths_smoothed',
            'new_cases_per_million', 'total_cases_per_million',
            'new_cases_smoothed_per_million', 'new_deaths_per_million',
            'total_deaths_per_million', 'new_deaths_smoothed_per_million'
        ]
        existing_redundant = [col for col in redundant_cols if col in data.columns]
        data.drop(columns=existing_redundant, inplace=True)
        for col in existing_redundant:
            print(f"Colonne supprimée (redondante) : {col}")

        # Conversion en entier pour les compteurs
        int_cols = ['total_cases', 'total_deaths', 'daily_new_cases', 'daily_new_deaths','active_cases']
        for col in int_cols:
            if col in data.columns:
                data[col] = data[col].astype('int64')

        # Tri et index reset
        data.sort_values(by=['country', 'date'], inplace=True)
        data.reset_index(drop=True, inplace=True)
>>>>>>> 84497e9cce70d33ec028c2e0e041b077d81c8ff2

        print("Transformation des données réussie.")
        return data

    except Exception as e:
        print(f"Erreur lors de la transformation : {e}")
        return None

<<<<<<< HEAD

# Load
=======
# --- Chargement ---
>>>>>>> 84497e9cce70d33ec028c2e0e041b077d81c8ff2
def load(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Données enregistrées dans : {output_file}")
        
        conn=connect_to_db()
        insert_daily_pandemic_country_data(conn,output_file,2)
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")
<<<<<<< HEAD


if __name__ == "__main__":
    input_file = "../donnes/owid-monkeypox-data.csv"
    output_file = "../donnes_clean/owid-monkeypox-data_clean.csv"

    # Processus ETL

    # Extraction
    raw_data = extract(input_file)

    # Transformation
=======
        
def process_monkeypox(file_path, output_file):
    raw_data = extract(file_path)
>>>>>>> 84497e9cce70d33ec028c2e0e041b077d81c8ff2
    if raw_data is not None:
        cleaned_data = transform(raw_data)
        if cleaned_data is not None:
            load(cleaned_data, output_file)

if __name__ == "__main__":
    input_file = "../donnes/owid-monkeypox-data.csv"
    output_file = "../donnes_clean/owid-monkeypox-data_clean.csv"
    process_monkeypox(input_file, output_file)

