import pandas as pd

# Extraction
def extract(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return None

# Transformation
def transform(data):
    try:
        # Suppression de la colonne 'iso_code'
        if 'iso_code' in data.columns:
            data = data.drop(columns=['iso_code'])
        
        # Renommer les colonnes
        data = data.rename(columns={
            'new_cases': 'daily_new_cases',
            'new_deaths': 'daily_new_deaths',
            'location': 'country'
        })
        
        # Filtrer les lignes où 'country' est l'une des valeurs suivantes : "Africa", "Europe", "North America", "South America", "Asia", "World"
        countries_to_remove = ["Africa", "Europe", "North America", "South America", "Asia", "World", "Puerto Rico"]
        data = data[~data['country'].isin(countries_to_remove)]
        
        # Modifier les noms de pays : "United States" => "US" et "United Kingdom" => "UK"
        data['country'] = data['country'].replace({"United States": "USA", "United Kingdom": "UK"})
        
        # Remplacer les espaces par des underscores dans 'country'
        data['country'] = data['country'].str.replace(" ", "_")
        
 
        data['country'] = data['country'].str.replace("Saint_Martin_(French_part)", "Saint_Martin")
        data['country'] = data['country'].str.replace("Democratic_Republic_of_Congo", "Democratic_Republic_Of_The_Congo")
        data['country'] = data['country'].str.replace("Vietnam", "Viet_Nam")
        data['country'] = data['country'].str.replace("Bosnia_and_Herzegovina", "Bosnia_And_Herzegovina")
        data['country'] = data['country'].str.replace("Czechia", "Czech_Republic")
        
        # Remplacer les valeurs manquantes par 0 pour les colonnes numériques
        numeric_columns = ['total_cases', 'total_deaths', 'daily_new_cases', 'daily_new_deaths', 
                           'new_cases_smoothed', 'new_deaths_smoothed', 'new_cases_per_million',
                           'total_cases_per_million', 'new_cases_smoothed_per_million', 
                           'new_deaths_per_million', 'total_deaths_per_million', 
                           'new_deaths_smoothed_per_million']
        
        data[numeric_columns] = data[numeric_columns].fillna(0)
        
        # Conversion des valeurs numériques en int
        data[numeric_columns] = data[numeric_columns].astype('int64')

        print("Transformation des données réussie.")
        return data

    except Exception as e:
        print(f"Erreur lors de la transformation : {e}")
        return None

# Load
def load(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Données nettoyées enregistrées dans : {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")

if __name__ == "__main__":
    input_file = "C:/Users/Anes/MSPR/donnes/owid-monkeypox-data.csv"
    output_file = "C:/Users/Anes/MSPR/donnes_clean/owid-monkeypox-data_clean.csv"

    # Processus ETL

    # Extraction
    raw_data = extract(input_file)

    # Transformation
    if raw_data is not None:
        cleaned_data = transform(raw_data)

        # Load
        if cleaned_data is not None:
            load(cleaned_data, output_file)
