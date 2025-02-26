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
        # Suppression des espaces dans les noms des pays
        data['country'] = data['country'].str.strip().str.replace(" ", "_")

        # Validation et conversion de la colonne 'date' en format datetime
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

        # Remplacement des valeurs numériques manquantes par 0
        numeric_columns = [
            'cumulative_total_cases', 
            'daily_new_cases', 
            'active_cases', 
            'cumulative_total_deaths', 
            'daily_new_deaths'
        ]
        data[numeric_columns] = data[numeric_columns].fillna(0)

        # Conversion des valeurs numériques en bigint (int64)
        for col in numeric_columns:
            data[col] = data[col].astype('int64')

        # Validation pour les valeurs négatives (remplacement par 0)
        for col in numeric_columns:
            data[col] = data[col].apply(lambda x: max(x, 0))

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
    input_file = "../donnes/worldometer_coronavirus_daily_data.csv"
    output_file = "../donnes_clean/worldometer_coronavirus_daily_clean.csv"

    # Processus ETL

    # Extraction
    raw_data = extract(input_file)

    # Transformation
    if raw_data is not None:
        cleaned_data = transform(raw_data)

        # Load
        if cleaned_data is not None:
            load(cleaned_data, output_file)
