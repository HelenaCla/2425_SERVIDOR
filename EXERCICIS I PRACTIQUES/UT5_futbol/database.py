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

def get_user_by_credentials(username: str, password: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, username, password, code
                FROM users
                WHERE username = %s AND password = %s
                LIMIT 1
            """
            cursor.execute(sql, (username, password))
            return cursor.fetchone()
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
