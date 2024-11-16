import pymysql.cursors
import datetime

class carrosdb(object):
    def conecta(self):
        # Conexión a la BBDD del servidor mySQL
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

    def insertarReserva(self, idcarro, iniciReserva, finalReserva, usuario):
        self.conecta()
        sql = "INSERT INTO reservas (idcarro, iniciReserva, finalReserva, usuario) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (idcarro, iniciReserva, finalReserva, usuario))
        ResQuery = self.cursor.fetchall()
        self.desconecta()
        return ResQuery
    
    def eliminaCarro(self, id):
        #Conexion a la BBDD del servidor mySQL
        db = self.conecta()
        cursor=db.cursor()
        sql="DELETE from carros WHERE id="+str(id)
        cursor.execute(sql)
        db.close()
    
#    def modificaEditor(self, iniciReserva):
#        db = self.conecta()
#        cursor=db.cursor()
#        sql="UPDATE editors SET NOM_EDIT='"+nom+"' WHERE id_edit="+str(id_edit)
#        cursor.execute(sql)
#        db.close()