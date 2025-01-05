from config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour créer la table NewCases
def create_NewCases_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS NewCases (
                    "DeathsID" SERIAL PRIMARY KEY,
                    "Country" VARCHAR(255) NOT NULL,
                    "WHORegion" VARCHAR(100),
                    "Date" DATE NOT NULL,
                    "daily_new_cases" INT NOT NULL,
                    FOREIGN KEY ("Country") REFERENCES Pays("Country") ON DELETE SET NULL,
                    FOREIGN KEY ("WHORegion") REFERENCES Region("WHORegion") ON DELETE SET NULL
                );
            """)
            conn.commit()
            print("Table NewCases vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table NewCases : {e}")


# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Créer la table NewCases
    create_NewCases_table(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
