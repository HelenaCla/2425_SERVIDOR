import pymysql.cursors 


class vols(object):
    def conecta(self):
        #Conexion a la BBDD del servidor mySQL
        self.db = pymysql.connect(host='localhost',
                                     user='root',
                                     db='vols',
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.db.cursor()

    def desconecta(self):
        self.db.close()

    def cargaAeroports(self):
        self.conecta()
        sql="SELECT * from airports"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery

    def cargaArribades(self, aeroport, fecha_hora):
        self.conecta()
        fechasql = fecha_hora.strftime("%Y-%m-%d")
        sql = ("SELECT *, (SELECT country FROM airports WHERE id_airport = flights.departure_airport) as departure_country, "
               "(SELECT country FROM airports WHERE id_airport = flights.arrival_airport) as arrival_country "
               "FROM flights WHERE arrival_airport = %s AND arrival_time >= %s ORDER BY arrival_time LIMIT 10")
        self.cursor.execute(sql, (aeroport, fechasql))
        ResQuery = self.cursor.fetchall()
        self.desconecta()
        return ResQuery

    def cargaSortides(self, aeroport, fecha_hora):
        self.conecta()
        fechasql = fecha_hora.strftime("%Y-%m-%d")
        sql = ("SELECT *, (SELECT country FROM airports WHERE id_airport = flights.departure_airport) as departure_country, "
               "(SELECT country FROM airports WHERE id_airport = flights.arrival_airport) as arrival_country "
               "FROM flights WHERE departure_airport = %s AND departure_time >= %s ORDER BY departure_time LIMIT 10")
        self.cursor.execute(sql, (aeroport, fechasql))
        ResQuery = self.cursor.fetchall()
        self.desconecta()
        return ResQuery