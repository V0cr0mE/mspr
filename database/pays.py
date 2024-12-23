from config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour créer la table Pays selon la structure du fichier 7
def create_country_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pays (
                    "id" SERIAL PRIMARY KEY,
                    "Country" VARCHAR(255) NOT NULL,
                    "Continent" VARCHAR(255),
                    "Population" INT,   
                    "RegionID" INT,
                    FOREIGN KEY ("RegionID") REFERENCES Region("RegionID") ON DELETE SET NULL            
                );
            """)
            conn.commit()
            print("Table Pays vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table Pays : {e}")

# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Créer la table Pays selon la structure du fichier 7
    create_country_table(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
