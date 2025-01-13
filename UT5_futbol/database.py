import pymysql
from pymysql.cursors import DictCursor

def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        db="futbol",
        charset="utf8mb4",
        cursorclass=DictCursor
    )
    return connection

def get_all_equipos():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, equipo FROM equipos")
            equipos = cursor.fetchall()
        return equipos
    finally:
        conn.close()

def get_resultats_por_equipo(id_equip: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT r.HomeTeam, e1.equipo AS HomeName,
                       r.AwayTeam, e2.equipo AS AwayName,
                       r.HomeGoals, r.AwayGoals
                FROM results r
                JOIN equipos e1 ON r.HomeTeam = e1.id
                JOIN equipos e2 ON r.AwayTeam = e2.id
                WHERE r.HomeTeam = %s OR r.AwayTeam = %s
                ORDER BY r.fecha ASC
            """
            cursor.execute(query, (id_equip, id_equip))
            return cursor.fetchall()
    finally:
        conn.close()

def check_match_exists(home_team_id: int, away_team_id: int) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT COUNT(*) AS count
                FROM results
                WHERE HomeTeam = %s AND AwayTeam = %s
            """
            cursor.execute(query, (home_team_id, away_team_id))
            row = cursor.fetchone()
            return row["count"] > 0
    finally:
        conn.close()

def insert_resultado(jornada: int, fecha: str, home_team: int, away_team: int, home_goals: int, away_goals: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO results (Jornada, fecha, HomeTeam, AwayTeam, HomeGoals, AwayGoals)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                jornada,
                fecha,
                home_team,
                away_team,
                home_goals,
                away_goals
            ))
        conn.commit()
    finally:
        conn.close()

def get_classification_query():
    sql = """
    SELECT 
        e.id AS id_equipo,
        e.equipo AS nom_equip,
        (
            SELECT COUNT(*) 
            FROM results r
            WHERE r.HomeTeam = e.id 
               OR r.AwayTeam = e.id
        ) AS Partits_Jugats,
        (
            SELECT COUNT(*)
            FROM results r
            WHERE (r.HomeTeam = e.id AND r.HomeGoals > r.AwayGoals)
               OR (r.AwayTeam = e.id AND r.AwayGoals > r.HomeGoals)
        ) AS Partits_Guanyats,
        (
            SELECT COUNT(*)
            FROM results r
            WHERE (r.HomeTeam = e.id AND r.HomeGoals = r.AwayGoals)
               OR (r.AwayTeam = e.id AND r.AwayGoals = r.HomeGoals)
        ) AS Partits_Empatats,
        (
            SELECT COUNT(*)
            FROM results r
            WHERE (r.HomeTeam = e.id AND r.HomeGoals < r.AwayGoals)
               OR (r.AwayTeam = e.id AND r.AwayGoals < r.HomeGoals)
        ) AS Partits_Perduts,
        (
            SELECT COALESCE(SUM(
                CASE 
                    WHEN r.HomeTeam = e.id THEN r.HomeGoals
                    WHEN r.AwayTeam = e.id THEN r.AwayGoals
                    ELSE 0
                END
            ), 0)
            FROM results r
            WHERE r.HomeTeam = e.id OR r.AwayTeam = e.id
        ) AS Gols_a_favor,
        (
            SELECT COALESCE(SUM(
                CASE
                    WHEN r.HomeTeam = e.id THEN r.AwayGoals
                    WHEN r.AwayTeam = e.id THEN r.HomeGoals
                    ELSE 0
                END
            ), 0)
            FROM results r
            WHERE r.HomeTeam = e.id OR r.AwayTeam = e.id
        ) AS Gols_en_contra,
        (
            3 * (
                SELECT COUNT(*)
                FROM results r
                WHERE (r.HomeTeam = e.id AND r.HomeGoals > r.AwayGoals)
                   OR (r.AwayTeam = e.id AND r.AwayGoals > r.HomeGoals)
            )
            +
            1 * (
                SELECT COUNT(*)
                FROM results r
                WHERE (r.HomeTeam = e.id AND r.HomeGoals = r.AwayGoals)
                   OR (r.AwayTeam = e.id AND r.AwayGoals = r.HomeGoals)
            )
        ) AS Punts
    FROM equipos e
    ORDER BY Punts DESC, Gols_a_favor DESC
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows
    finally:
        conn.close()
