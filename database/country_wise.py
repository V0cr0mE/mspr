from config_db import connect_to_db
import pandas as pd
import numpy as np

# Connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Charger les données depuis un fichier CSV
def load_data_from_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return None

# Nettoyer les données : remplacer les valeurs infinies et NaN par None (NULL) ou 0
def clean_data(data):
    data.replace([np.inf, -np.inf], None, inplace=True)  # Remplacer les infinis par None
    data.fillna(0, inplace=True)  # Remplacer les NaN par 0
    return data

# Renommer les colonnes pour correspondre à la structure de la table SQL
def rename_columns(data):
    data.columns = [
        "CountryRegion", "Confirmed", "Deaths", "Recovered", "Active",
        "NewCases", "NewDeaths", "NewRecovered", "DeathsPer100Cases",
        "RecoveredPer100Cases", "DeathsPer100Recovered", "ConfirmedLastWeek",
        "OneWeekChange", "OneWeekPercentageIncrease", "WHORegion"
    ]
    return data

# Créer la table 'CovidStatistics' si elle n'existe pas
def create_covid_statistics_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT to_regclass('public.CovidStatistics');
            """)
            result = cursor.fetchone()
            if result[0] is None:
                cursor.execute("""
                    CREATE TABLE CovidStatistics (
                        "CountryRegion" VARCHAR(100) PRIMARY KEY,
                        "Confirmed" INT,
                        "Deaths" INT,
                        "Recovered" INT,
                        "Active" INT,
                        "NewCases" INT,
                        "NewDeaths" INT,
                        "NewRecovered" INT,
                        "DeathsPer100Cases" DECIMAL(10,2),
                        "RecoveredPer100Cases" DECIMAL(10,2),
                        "DeathsPer100Recovered" DECIMAL(10,2),
                        "ConfirmedLastWeek" INT,
                        "OneWeekChange" INT,
                        "OneWeekPercentageIncrease" DECIMAL(10,2),
                        "WHORegion" VARCHAR(100)
                    );
                """)
                conn.commit()
                print("Table créée avec succès avec la clé primaire.")
            else:
                print("La table existe déjà.")
    except Exception as e:
        print(f"Erreur lors de la création ou modification de la table : {e}")
        conn.close()
        exit()

# Insérer les données dans la table 'CovidStatistics'
def insert_data_into_covid_statistics(conn, data):
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO CovidStatistics (
                    "CountryRegion", "Confirmed", "Deaths", "Recovered", "Active",
                    "NewCases", "NewDeaths", "NewRecovered", "DeathsPer100Cases",
                    "RecoveredPer100Cases", "DeathsPer100Recovered", "ConfirmedLastWeek",
                    "OneWeekChange", "OneWeekPercentageIncrease", "WHORegion"
                ) 
                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM CovidStatistics WHERE "CountryRegion" = %s
                );
            """
            # Exécution de la requête d'insertion pour chaque ligne
            for row in data.values:
                cursor.execute(insert_query, (*row, row[0]))  # row[0] est "CountryRegion"
            conn.commit()
            print("Données insérées avec succès sans doublons.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")

# Vérifier si les données ont été insérées correctement
def verify_insertions(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM CovidStatistics;")
            result = cursor.fetchone()
            print(f"Nombre de lignes insérées : {result[0]}")
    except Exception as e:
        print(f"Erreur lors de la vérification des données : {e}")

# Programme principal
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Charger et nettoyer les données
    file_path = "C:/Users/Anes/Downloads/country_wise_latest.csv" 
    data = load_data_from_csv(file_path)
    if data is None:
        conn.close()
        return

    data = clean_data(data)
    data = rename_columns(data)

    # Créer la table si elle n'existe pas
    create_covid_statistics_table(conn)

    # Insérer les données dans la base
    insert_data_into_covid_statistics(conn, data)

    # Vérifier les données insérées
    verify_insertions(conn)

    # Fermeture de la connexion à la base de données
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
