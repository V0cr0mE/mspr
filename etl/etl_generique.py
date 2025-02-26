import pandas as pd
import os


# Extraction
def extract(file_path):
    try:
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            data = pd.read_json(file_path)
        else:
            print(f"Format de fichier non supporté: {file_path}")
            return None
        print(f"Extraction réussie pour {file_path}")
        return data
    except Exception as e:
        print(f"Erreur lors de l'extraction de {file_path} : {e}")
        return None


# Transformation
def transform(data, file_type):
    try:
        if file_type == "worldometer_daily":
            data["country"] = data["country"].str.strip().str.replace(" ", "_")
            data["country"] = data["country"].str.lower()
            data["date"] = pd.to_datetime(data["date"], errors="coerce")
            numeric_columns = [
                "cumulative_total_cases",
                "daily_new_cases",
                "active_cases",
                "cumulative_total_deaths",
                "daily_new_deaths",
            ]

        elif file_type == "worldometer_summary":
            data["country"] = data["country"].str.replace(" ", "_")
            data["country"] = data["country"].str.lower()
            data["continent"] = data["continent"].str.replace(" ", "_")
            data["continent"] = data["continent"].str.lower()
            numeric_columns = [
                "total_confirmed",
                "total_deaths",
                "total_recovered",
                "active_cases",
                "serious_or_critical",
                "total_cases_per_1m_population",
                "total_deaths_per_1m_population",
                "total_tests",
                "total_tests_per_1m_population",
                "population",
            ]

        elif file_type == "monkeypox":
            data = data.drop(columns=["iso_code"], errors="ignore")
            data = data.rename(
                columns={
                    "new_cases": "daily_new_cases",
                    "new_deaths": "daily_new_deaths",
                    "location": "country",
                }
            )
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
            data["country"] = data["country"].replace(
                {
                    "United States": "USA",
                    "United Kingdom": "UK",
                    "Saint Martin (French part)": "Saint_Martin",
                    "Democratic Republic of Congo": "Democratic_Republic_Of_The_Congo",
                    "Vietnam": "Viet_Nam",
                    "Bosnia and Herzegovina": "Bosnia_And_Herzegovina",
                    "Czechia": "Czech_Republic",
                }
            )
            data["country"] = data["country"].str.replace(" ", "_")
            data["country"] = data["country"].str.lower()
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

        else:
            print("Type de fichier non reconnu.")
            return None

        data[numeric_columns] = data[numeric_columns].fillna(0)
        data[numeric_columns] = data[numeric_columns].astype("int64")
        data = data.drop_duplicates()
        data[numeric_columns] = data[numeric_columns].apply(lambda x: x.clip(lower=0))
        print(f"Transformation réussie pour {file_type}")
        return data
    except Exception as e:
        print(f"Erreur lors de la transformation de {file_type} : {e}")
        return None


# Load
def load(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Données nettoyées enregistrées dans : {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")


if __name__ == "__main__":
    files = [
        ("../donnes/worldometer_coronavirus_daily_data.csv", "worldometer_daily"),
        ("../donnes/worldometer_coronavirus_summary_data.csv", "worldometer_summary"),
        ("../donnes/owid-monkeypox-data.csv", "monkeypox"),
    ]
    output_dir = "../donnes_clean/"

    for file_path, file_type in files:
        raw_data = extract(file_path)
        if raw_data is not None:
            cleaned_data = transform(raw_data, file_type)
            if cleaned_data is not None: 
                output_file = os.path.join(
                    output_dir,
                    os.path.basename(file_path).replace(".csv", "_clean.csv"),
                )
                load(cleaned_data, output_file)
