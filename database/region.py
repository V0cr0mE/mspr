from config_db import connect_to_db, host, dbname, user, password, port
import pandas as pd
from sqlalchemy import create_engine

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour charger les données depuis le fichier CSV
def load_csv_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return None

# Fonction pour créer la table si elle n'existe pas
def create_region_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Region (
                    "WHORegion" VARCHAR(100) PRIMARY KEY
                );
            """)
            conn.commit()
            print("Table Region vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table Region : {e}")

# Fonction pour insérer les données dans la table Region
def insert_regions(conn, regions):
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO Region ("WHORegion")
                VALUES (%s)
                ON CONFLICT ("WHORegion") DO NOTHING;
            """
            for region in regions:
                cursor.execute(insert_query, (region,))
            conn.commit()
            print("Données insérées dans la table Region avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")

# Fonction pour ajouter la clé étrangère à la table CovidStatistics
def add_foreign_key(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                ALTER TABLE CovidStatistics
                ADD CONSTRAINT fk_region
                FOREIGN KEY ("WHORegion") REFERENCES Region("WHORegion")
                ON DELETE SET NULL;
            """)
            conn.commit()
            print("Clé étrangère ajoutée avec succès entre CovidStatistics et Region.")
    except Exception as e:
        print(f"Erreur lors de l'ajout de la clé étrangère : {e}")

# Fonction pour vérifier le nombre de régions insérées
def verify_insertions(engine):
    try:
        query = "SELECT COUNT(*) FROM Region;"
        result = pd.read_sql(query, con=engine)
        print(f"Nombre de régions insérées : {result.iloc[0, 0]}")
    except Exception as e:
        print(f"Erreur lors de la vérification des insertions : {e}")

# Fonction principale pour exécuter le processus complet
def main():
    # Paramètres de la base de données
    file_path = "C:/Users/Anes/Downloads/country_wise_latest.csv"
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")
    
    # Connexion à la base de données
    conn = connect_to_database()

    # Charger les données depuis le fichier CSV
    data = load_csv_data(file_path)
    if data is None:
        conn.close()
        return

    # Renommer les colonnes pour correspondre à la structure de la base de données
    data.columns = [
        "CountryRegion", "Confirmed", "Deaths", "Recovered", "Active",
        "NewCases", "NewDeaths", "NewRecovered", "DeathsPer100Cases",
        "RecoveredPer100Cases", "DeathsPer100Recovered", "ConfirmedLastWeek",
        "OneWeekChange", "OneWeekPercentageIncrease", "WHORegion"
    ]

    # Extraire les valeurs uniques de la colonne WHORegion
    unique_regions = data["WHORegion"].unique()

    # Créer la table Region si nécessaire
    create_region_table(conn)

    # Insérer les régions dans la table
    insert_regions(conn, unique_regions)

    # Ajouter la clé étrangère entre CovidStatistics et Region
    add_foreign_key(conn)

    # Vérifier les insertions
    verify_insertions(engine)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
