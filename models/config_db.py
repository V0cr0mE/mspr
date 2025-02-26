import psycopg2
# Paramètres de connexion à la base de données
host = "localhost"
dbname = "covid"
user = "postgres"
password = "Chichibald76."
port = "5433"

print("Connexion réussie à la base de données.")

# Fonction de connexion à la base de données
def connect_to_db():
    try:
        print("Try Connexion réussie à la base de données.")
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        print("Connexion réussie à la base de données.")
        return conn
    except BaseException as e:
        print(f"Erreur de connexion : {e}")
        exit()
