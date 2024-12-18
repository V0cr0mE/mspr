
from config_db import connect_to_db, host, dbname, user, password, port
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# Connexion à la base de données
conn = connect_to_db()

# Charger les données depuis un fichier CSV
file_path = "C:/Users/Anes/Downloads/country_wise_latest.csv"  # Chemin vers votre fichier CSV
try:
    data = pd.read_csv(file_path)
    print("Fichier chargé avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du fichier : {e}")
    conn.close()
    exit()

# Vérification du contenu des données
print("Affichage des premières lignes du fichier CSV chargé:")
print(data.head())

# Nettoyer les données : remplacer les valeurs infinies et NaN par None (NULL) ou 0
data.replace([np.inf, -np.inf], None, inplace=True)  # Remplacer les infinis par None
data.fillna(0, inplace=True)  # Remplacer les NaN par 0

# Renommer les colonnes pour qu'elles correspondent à la table SQL
data.columns = [
    "CountryRegion", "Confirmed", "Deaths", "Recovered", "Active",
    "NewCases", "NewDeaths", "NewRecovered", "DeathsPer100Cases",
    "RecoveredPer100Cases", "DeathsPer100Recovered", "ConfirmedLastWeek",
    "OneWeekChange", "OneWeekPercentageIncrease", "WHORegion"
]

# Convertir chaque ligne du DataFrame en un tuple
tuples_data = [tuple(row) for row in data.values]

# Création d'un moteur SQLAlchemy pour faciliter l'insertion dans la base de données
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

# Vérification de l'existence de la table et modification si nécessaire
try:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT to_regclass('public.CovidStatistics');
        """)
        result = cursor.fetchone()
        if result[0] is None:
            # La table n'existe pas, on la crée avec la clé primaire
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
            # La table existe déjà, on vérifie si la clé primaire existe
            cursor.execute("""
                SELECT conname
                FROM pg_constraint
                WHERE conrelid = 'public.CovidStatistics'::regclass
                  AND contype = 'p';
            """)
            primary_key = cursor.fetchone()
            if not primary_key:
                # Ajouter la clé primaire si elle n'existe pas
                cursor.execute("""
                    ALTER TABLE CovidStatistics
                    ADD PRIMARY KEY ("CountryRegion");
                """)
                conn.commit()
                print("Clé primaire ajoutée à la table existante.")
            else:
                print("La clé primaire existe déjà sur la table.")
except Exception as e:
    print(f"Erreur lors de la vérification ou modification de la table : {e}")
    conn.close()
    exit()

# Insérer les données sous forme de tuples dans la base de données avec psycopg2
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
        for row in tuples_data:
            cursor.execute(insert_query, (*row, row[0]))
        conn.commit()
        print("Données insérées avec succès sans doublons.")
except Exception as e:
    print(f"Erreur lors de l'insertion des données : {e}")

# Vérifier si les données ont été insérées correctement
try:
    print("Vérification des données dans la table:")
    query = "SELECT COUNT(*) FROM CovidStatistics;"
    result = pd.read_sql(query, con=engine)
    print(f"Nombre de lignes insérées : {result.iloc[0, 0]}")
except Exception as e:
    print(f"Erreur lors de la vérification des données : {e}")

# Fermeture de la connexion à la base de données
conn.close()
print("Connexion à la base de données fermée.")
