from config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour créer la table Deces
def create_deces_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Deces (
                    "DecesID" SERIAL PRIMARY KEY,
                    "CountryID" INT NOT NULL,
                    "RegionID" INT,
                    "Date" DATE NOT NULL,
                    "NombreDeces" INT NOT NULL,
                    FOREIGN KEY ("CountryID") REFERENCES Pays("id") ON DELETE SET NULL,
                    FOREIGN KEY ("RegionID") REFERENCES Region("RegionID") ON DELETE SET NULL
                );
            """)
            conn.commit()
            print("Table Deces vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table Deces : {e}")


# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Créer la table Deces
    create_deces_table(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
