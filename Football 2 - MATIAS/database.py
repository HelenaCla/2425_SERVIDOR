import pymysql.cursors
import sqlalchemy as db

class Football(object):
    def conecta(self):
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            db="futbol",
            charset="utf8mb4",
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.db.cursor()

    def desconecta(self):
        self.db.close()

    def checkUser(self, username):
        sql = """
        SELECT *
        FROM usuaris
        WHERE username = %s
        """
        self.cursor.execute(sql, (username,))
        user_data = self.cursor.fetchone()
        return user_data

    
    def cargaEquipsAll(self):
        sql = "SELECT * FROM equipos"
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def cargaResultatsEquip(self, id_equip):
        sql = """
        SELECT 
            home.equipo AS local,
            away.equipo AS visitant,
            CONCAT(r.HomeGoals, '-', r.AwayGoals) AS resultat
        FROM 
            results r
        INNER JOIN 
            equipos home ON r.HomeTeam = home.id
        INNER JOIN 
            equipos away ON r.AwayTeam = away.id
        WHERE 
            r.HomeTeam = %s OR r.AwayTeam = %s
        """
        self.cursor.execute(sql, (id_equip, id_equip))
        resultats = self.cursor.fetchall()
        return resultats

    
    def nouResultat(self, resultat):
        sql = "SELECT * FROM results WHERE (Fecha = %s AND HomeTeam = %s AND AwayTeam = %s)"
        self.cursor.execute(sql, (resultat.Fecha, resultat.HomeTeam, resultat.AwayTeam))
        check = self.cursor.fetchall()
        if check:
            return False
        else:
            sql = """
            INSERT INTO results (Jornada, Fecha, HomeTeam, AwayTeam, HomeGoals, AwayGoals)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (
                resultat.Jornada,
                resultat.Fecha,
                resultat.HomeTeam,
                resultat.AwayTeam,
                resultat.HomeGoals,
                resultat.AwayGoals
            ))
            return True

    
    def get_classificacio(self):
        sql = """
        SELECT 
            e.equipo AS nom_equip,
            COUNT(*) AS partits_jugats,
            SUM(CASE 
                WHEN r.HomeGoals > r.AwayGoals AND e.id = r.HomeTeam THEN 1
                WHEN r.AwayGoals > r.HomeGoals AND e.id = r.AwayTeam THEN 1
                ELSE 0
            END) AS partits_guanyats,
            SUM(CASE 
                WHEN r.HomeGoals = r.AwayGoals THEN 1
                ELSE 0
            END) AS partits_empatats,
            SUM(CASE 
                WHEN r.HomeGoals < r.AwayGoals AND e.id = r.HomeTeam THEN 1
                WHEN r.AwayGoals < r.HomeGoals AND e.id = r.AwayTeam THEN 1
                ELSE 0
            END) AS partits_perduts,
            SUM(CASE 
                WHEN e.id = r.HomeTeam THEN r.HomeGoals
                WHEN e.id = r.AwayTeam THEN r.AwayGoals
                ELSE 0
            END) AS gols_a_favor,
            SUM(CASE 
                WHEN e.id = r.HomeTeam THEN r.AwayGoals
                WHEN e.id = r.AwayTeam THEN r.HomeGoals
                ELSE 0
            END) AS gols_en_contra,
            (SUM(CASE 
                WHEN r.HomeGoals > r.AwayGoals AND e.id = r.HomeTeam THEN 2
                WHEN r.AwayGoals > r.HomeGoals AND e.id = r.AwayTeam THEN 2
                WHEN r.HomeGoals < r.AwayGoals AND e.id = r.HomeTeam THEN -1
                WHEN r.AwayGoals < r.HomeGoals AND e.id = r.AwayTeam THEN -1
                ELSE 0
            END)) AS punts
        FROM 
            equipos e
        LEFT JOIN 
            results r
        ON 
            e.id = r.HomeTeam OR e.id = r.AwayTeam
        GROUP BY 
            e.id
        ORDER BY 
            punts DESC, gols_a_favor DESC, gols_en_contra ASC;
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
