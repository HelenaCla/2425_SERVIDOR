import pymysql.cursors
import datetime

class carrosdb(object):
    def conecta(self):
        # Conexió a la BBDD del servidor mySQL
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            db='rentacarro',
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.db.cursor()
    
    def desconecta(self):
        self.db.close()

    def cargarCarros(self):
        self.conecta()
        sql = "SELECT * FROM carros"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        self.desconecta()
        return ResQuery
#Funció per insertar reserves
    def insertarReserva(self, idcarro, iniciReserva, finalReserva, usuario):
        self.conecta()
        sql = "INSERT INTO reservas (idcarro, iniciReserva, finalReserva, usuario) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (idcarro, iniciReserva, finalReserva, usuario))
        ResQuery = self.cursor.fetchall()
        self.desconecta()
        return ResQuery
    
#Funció per mostrar les reserves
    def mostraReserves(self, start_date, end_date):
        self.conecta()
        sql = """SELECT carros.id AS idcarro, carros.nom AS nombreCarro, reservas.usuario, reservas.iniciReserva, reservas.finalReserva FROM reservas
        JOIN carros ON reservas.idcarro = carros.id
        WHERE reservas.iniciReserva BETWEEN %s AND %s
        """
        self.cursor.execute(sql, (start_date, end_date))
        ResQuery=self.cursor.fetchall()
        self.desconecta()
        return ResQuery;
#Funció per eliminar Carros  
    def eliminaCarro(self, id):
        self.conecta()
        sqlReserva = "DELETE FROM reservas WHERE idcarro = %s"
        self.cursor.execute(sqlReserva, (id,))
        sqlCarro = "DELETE FROM carros WHERE id = %s"
        self.cursor.execute(sqlCarro, (id,))
        self.desconecta()
#Funció per modificar Carros
    def modificaCarro(self, idcarro, nom, descripcio, classe, preu, img):
        self.conecta()
        sql = """
        UPDATE carros
        SET nom = %s, descripcio = %s, clase = %s, preu = %s, img = %s
        WHERE id = %s
        """
        self.cursor.execute(sql, (nom, descripcio, classe, preu, img, idcarro))
        self.desconecta()
    
#Funció per crear carros
    def crearCarro(self, nom, descripcio, classe, preu, img ):
        self.conecta()
        sql = "INSERT INTO carros (nom, descripcio, clase, preu, img) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (nom, descripcio, classe, preu, img))
        self.desconecta()
        
#Funció per comprovar disponibilitat
    def comprDispo(self, idcarro, iniciReserva, finalReserva):
        self.conecta()
        sql = """
        SELECT * FROM reservas
        WHERE idcarro = %s 
        AND (
            (iniciReserva <= %s AND finalReserva >= %s) OR 
            (iniciReserva <= %s AND finalReserva >= %s)
        )
        """
        self.cursor.execute(sql, (idcarro, finalReserva, finalReserva, iniciReserva, iniciReserva))
        ocupada = self.cursor.fetchone()
        self.desconecta()
        return ocupada is None  # Si es None, está disponible
    
    def mostraCarroPerId(self, idCarro):
        self.conecta()
        sql = "SELECT * FROM carros WHERE id = %s"
        self.cursor.execute(sql, (idCarro,))
        carro = self.cursor.fetchone()
        self.desconecta()
        return carro
    
    def calculaCost(self, idcarro, iniciReserva, finalReserva):
        self.conecta()
        sql = "SELECT preu FROM carros WHERE id = %s"
        self.cursor.execute(sql, (idcarro,))
        carro = self.cursor.fetchone()
        self.desconecta()
        
        if carro:
            preuDiari = carro['preu']
            delta = finalReserva - iniciReserva
            dies = delta.days
            if delta.seconds > 0:  # Si hay menos de 24 horas, añadir un día extra
                dies += 1
            return dies * preuDiari
        return 0