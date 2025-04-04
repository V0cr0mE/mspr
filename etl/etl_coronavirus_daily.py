import pandas as pd

# Extraction
def extract(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return None

# Transformation
def transform(data):
    try:
        # Nettoyage des noms de pays
        data['country'] = data['country'].str.strip().str.replace(" ", "_")

        # Conversion de la date
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

        # Colonnes à remplir par 0
        zero_cols = ['daily_new_cases', 'daily_new_deaths']
        for col in zero_cols:
            if col in data.columns:
                data[col].fillna(0, inplace=True)
                data[col] = data[col].apply(lambda x: max(x, 0)).astype('int64')

        # Recalcul ou nettoyage de active_cases
        if 'active_cases' in data.columns:
            data['active_cases'] = data['active_cases'].fillna(0)
            data['active_cases'] = data['active_cases'].apply(lambda x: max(x, 0)).astype('int64')

        # Suppression des colonnes cumulatives si présentes
        cumulative_cols = ['cumulative_total_cases', 'cumulative_total_deaths']
        for col in cumulative_cols:
            if col in data.columns:
                data.drop(columns=col, inplace=True)
                print(f"Colonne supprimée : {col}")

        # Tri et réinitialisation
        data.sort_values(by=['country', 'date'], inplace=True)
        data.reset_index(drop=True, inplace=True)

        print("ransformation terminée.")
        return data
    except Exception as e:
        print(f"Erreur de transformation : {e}")
        return None

# Load
def load_daily(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Données enregistrées dans : {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")

# Main ETL process
if __name__ == "__main__":
    input_file = "C:/Users/Anes/MSPR/donnes/worldometer_coronavirus_daily_data.csv"
    output_file = "C:/Users/Anes/MSPR/donnes_clean/worldometer_coronavirus_daily_data_clean.csv"

    raw_data = extract(input_file)
    if raw_data is not None:
        cleaned_data = transform(raw_data)
        if cleaned_data is not None:
            load_daily(cleaned_data, output_file)
