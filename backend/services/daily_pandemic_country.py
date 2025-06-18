from models.config_db import connect_to_db

# Récupérer les données journalières pour un pays, une pandémie et une date spécifique
def get_daily_data(id_country, id_pandemic, date=None):
    conn = connect_to_db()
    query = """
        SELECT * FROM daily_pandemic_country 
        WHERE "id_country" = %s AND "id_pandemic" = %s
    """
    params = [id_country, id_pandemic]
    
    if date:
        query += " AND \"date\" = %s"
        params.append(date)
    
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        daily_data = [
            {
                "id_country": row[0],
                "id_pandemic": row[1],
                "date": row[2].strftime('%Y-%m-%d'),
                "active_cases": row[3],
                "daily_new_deaths": row[4],
                "daily_new_cases": row[5]
            }
            for row in rows
        ]
    conn.close()
    return daily_data


# Ajouter des données journalières
def add_daily_data(id_country, id_pandemic, date, daily_new_deaths, daily_new_cases,active_cases):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO daily_pandemic_country ("id_country", "id_pandemic", "date", "daily_new_deaths", "daily_new_cases","active_cases")
            VALUES (%s, %s, %s, %s, %s,%s)
            ON CONFLICT DO NOTHING;
        """, (id_country, id_pandemic, date, daily_new_deaths, daily_new_cases,active_cases))
    conn.commit()
    conn.close()

# Mettre à jour des données journalières
def update_daily_data(id_country, id_pandemic, date, daily_new_deaths, daily_new_cases,active_cases):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE daily_pandemic_country
            SET "daily_new_deaths" = %s, "daily_new_cases" = %s,"active_cases=%s
            WHERE "id_country" = %s AND "id_pandemic" = %s AND "date" = %s
        """, (daily_new_deaths, daily_new_cases,active_cases, id_country, id_pandemic, date))
    conn.commit()
    conn.close()

# Supprimer des données journalières
def delete_daily_data(id_country, id_pandemic, date):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM daily_pandemic_country
            WHERE "id_country" = %s AND "id_pandemic" = %s AND "date" = %s
        """, (id_country, id_pandemic, date))
    conn.commit()
    conn.close()

# Récupérer la dernière date disponible pour chaque pays pour une pandémie
# Renvoie une liste de dicts avec id_country, country name, date, daily_new_cases, daily_new_deaths

def get_latest_data_all_countries(id_pandemic):
    conn = connect_to_db()
    query = """
        SELECT DISTINCT ON (d.id_country) d.id_country, c.country, d.date,
               d.daily_new_cases, d.daily_new_deaths
        FROM daily_pandemic_country d
        JOIN country c ON d.id_country = c.id_country
        WHERE d.id_pandemic = %s
        ORDER BY d.id_country, d.date DESC;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (id_pandemic,))
        rows = cursor.fetchall()
        data = [
            {
                "id_country": row[0],
                "country": row[1],
                "date": row[2].strftime('%Y-%m-%d'),
                "daily_new_cases": row[3],
                "daily_new_deaths": row[4]
            }
            for row in rows
        ]
    conn.close()
    return data
