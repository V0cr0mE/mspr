from models.config_db import connect_to_db

# Récupérer tous les pays
def get_all_countries():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM country;")
        countries = cursor.fetchall()
    conn.close()
    return countries

# Ajouter un pays
def add_country(country_name, population, id_continent):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO country (country, population, "Id_continent")
            VALUES (%s, %s, %s)
            ON CONFLICT (country) DO NOTHING;
        """, (country_name, population, id_continent))
    conn.commit()
    conn.close()

# Supprimer un pays
def delete_country(id_country):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM country WHERE \"id_country\" = %s;", (id_country,))
    conn.commit()
    conn.close()

# Mettre à jour un pays
def update_country(id_country, country_name, population, id_continent):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE country
            SET country = %s, population = %s, "Id_continent" = %s
            WHERE "id_country" = %s;
        """, (country_name, population, id_continent, id_country))
    conn.commit()
    conn.close()
