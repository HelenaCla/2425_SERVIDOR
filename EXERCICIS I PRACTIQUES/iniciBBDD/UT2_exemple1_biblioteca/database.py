import pymysql.cursors

class Biblioteca(object):

    def cargaDepartaments():
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='biblioteca',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT * from departaments"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    def cargaLlibres(departament):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='biblioteca',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT llibres.titol,autors.nom_aut from llibres,autors,lli_aut WHERE lli_aut.FK_IDLLIB=llibres.ID_LLIB AND"
        sql=sql+" lli_aut.FK_IDAUT=autors.ID_AUT AND llibres.FK_DEPARTAMENT='"+departament+"';"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery
