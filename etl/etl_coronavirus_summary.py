import pandas as pd
from datetime import datetime
import numpy as np

# Extraction
def extract(file_path):
  
    try:
        data = pd.read_csv(file_path)
        print("Extraction réussie.")
        return data
    except Exception as e:
        print(f"Erreur lors de l'extraction : {e}")
        return None

# Transformation
def transform(data):
    
    try:
        # Supprimer les espaces dans les noms de pays et de continents
        data['country'] = data['country'].str.replace(" ", "_")
        data['continent'] = data['continent'].str.replace(" ", "_")

        # Remplacer les valeurs numériques manquantes par 0
        numeric_columns = [
            'total_confirmed', 'total_deaths', 'total_recovered', 
            'active_cases', 'serious_or_critical', 
            'total_cases_per_1m_population', 'total_deaths_per_1m_population', 
            'total_tests', 'total_tests_per_1m_population', 'population'
        ]
        data[numeric_columns] = data[numeric_columns].fillna(0)

        # S'assurer que les colonnes numériques sont de type bigint
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0).astype('int64')

        # Vérifier et corriger les valeurs négatives
        for col in numeric_columns:
            data[col] = data[col].apply(lambda x: max(x, 0))

        print("Nettoyage terminé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur lors du nettoyage des données : {e}")
        return None

# Load
def load(data, output_file):
    
    try:
        data.to_csv(output_file, index=False)
        print(f"Données sauvegardées dans le fichier : {output_file}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")


# Processus principal
def run_etl():
    # Chemin du fichier source
    file_path = "C:/Users/Anes/MSPR/donnes/worldometer_coronavirus_summary_data.csv"
    output_file = "C:/Users/Anes/MSPR/donnes_clean/worldometer_coronavirus_summary_clean.csv"

    # Extraction
    raw_data = extract(file_path)

    # Transformation
    if raw_data is not None:
        cleaned_data = transform(raw_data)

        # Load
        if cleaned_data is not None:
            load(cleaned_data, output_file)
