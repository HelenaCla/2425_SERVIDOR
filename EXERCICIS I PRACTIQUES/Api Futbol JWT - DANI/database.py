import pymysql.cursors

class futbol:
    def conecta(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            db='futbol',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.db.cursor()

    def desconecta(self):
        self.db.close()

    def cargaEquipos(self):
        sql = "SELECT * FROM equipos"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def cargaResultadosEquipo(self, id_equipo):
        sql = """
            SELECT 
                e1.equipo AS HomeTeam, 
                e2.equipo AS AwayTeam, 
                CONCAT(r.HomeGoals, '-', r.AwayGoals) AS Resultat
            FROM results r
            JOIN equipos e1 ON r.HomeTeam = e1.id
            JOIN equipos e2 ON r.AwayTeam = e2.id
            WHERE r.HomeTeam = %s OR r.AwayTeam = %s
        """
        self.cursor.execute(sql, (id_equipo, id_equipo))
        return self.cursor.fetchall()

    def añadirResultado(self, home_team, away_team, home_goals, away_goals, jornada, fecha):
        sql_check = "SELECT * FROM results WHERE HomeTeam = %s AND AwayTeam = %s AND fecha = %s"
        self.cursor.execute(sql_check, (home_team, away_team, fecha))
        if self.cursor.fetchone():
            return {"message": "El partido ya existe."}

        sql_insert = """
            INSERT INTO results (HomeTeam, AwayTeam, HomeGoals, AwayGoals, Jornada, fecha) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(sql_insert, (home_team, away_team, home_goals, away_goals, jornada, fecha))
            self.db.commit()
            return {"message": "Resultado añadido correctamente."}
        except Exception as e:
            return {"message": f"Error al añadir el resultado: {str(e)}"}

    def clasificacion(self):
        sql = """
        SELECT 
            e.id AS id_equipo,
            e.equipo AS nom_equip,
            (
                SELECT COUNT(*) 
                FROM results r
                WHERE r.HomeTeam = e.id OR r.AwayTeam = e.id
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
                SELECT COALESCE(SUM(CASE WHEN r.HomeTeam = e.id THEN r.HomeGoals ELSE r.AwayGoals END), 0)
                FROM results r
                WHERE r.HomeTeam = e.id OR r.AwayTeam = e.id
            ) AS Gols_a_favor,
            (
                SELECT COALESCE(SUM(CASE WHEN r.HomeTeam = e.id THEN r.AwayGoals ELSE r.HomeGoals END), 0)
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
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def cargaUsuarios(self):
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_user_by_username(self, username):
        sql = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(sql, (username,))
        return self.cursor.fetchone()
