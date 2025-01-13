import pymysql.cursors
import sqlalchemy as db
import configparser

class biblioteca(object):
    def conecta(self):
        #Conexion a la BBDD del servidor mySQL
        self.db = pymysql.connect(host='localhost',
                                     user='root',
                                     db='biblioteca',
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.db.cursor()

    def desconecta(self):
        self.db.close()

    def cargaEditoresAll(self):
        sql="SELECT * from editors"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery

    def cargaEditor(self,id_editor):
        sql="SELECT * from editors WHERE id_edit="+str(id_editor)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        return ResQuery

    def cargaLlibreid(self,id_llibre):
        sql="SELECT * from llibres where id_llib="+str(id_llibre)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        return ResQuery

    def cargaLlibreAutor(self,id_autor):
        sql="SELECT llibres.* from llibres,lli_aut WHERE lli_aut.FK_IDLLIB=llibres.ID_LLIB ";
        sql=sql+" AND lli_aut.FK_IDAUT="+str(id_autor)
        self.cursor.execute(sql)
        llibres=self.cursor.fetchall()
        return llibres

    def nouEditor(self,nouEDITOR):
        sql="SELECT MAX(ID_EDIT)+1 newid from editors";
        self.cursor.execute(sql)
        newid=self.cursor.fetchone()
        sql="insert into editors (ID_EDIT,NOM_EDIT) VALUES ("+str(newid['newid'])+",'"+nouEDITOR+"');"
        self.cursor.execute(sql)
        return newid['newid']        

    def esborraEditor(self,id_edit):
        sql="DELETE from editors WHERE ID_EDIT="+str(id_edit);
        self.cursor.execute(sql)

    def modificaEditor(self,id_edit,nouEditor):
        sql="UPDATE editors SET NOM_EDIT='"+nouEditor+"' WHERE ID_EDIT="+str(id_edit)
        self.cursor.execute(sql)