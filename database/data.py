import psycopg2

host = "localhost"
dbname = "covid" 
user = "postgres" 
password = "msprepsi"
port = "5432" 

try:
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )

    print("Connexion réussie à la base de données.")

    conn.close()
    
except Exception as e:
    print(f"Erreur de connexion : {e}")
