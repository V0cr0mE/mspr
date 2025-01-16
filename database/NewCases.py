from config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour créer la table newcases
def create_newcases_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS newcases (
                    "id_newcase" SERIAL PRIMARY KEY,
                    "id_country" INT,
                    "id_pandemic" INT,
                    "Date" DATE,
                    "daily_new_cases" BIGINT,
                    FOREIGN KEY ("id_country") REFERENCES country("id_country"),
                    FOREIGN KEY ("id_pandemic") REFERENCES pandemic("id_pandemic")
                );
            """)
            conn.commit()
            print("Table newcases vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table newcases : {e}")


# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Créer la table NewCases
    create_newcases_table(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
