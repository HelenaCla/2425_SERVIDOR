import pymysql.cursors

def conecta(self):
    self.db = pymysql.connect(
        host='localhost',
        user='root',
        db='whatsap',
        charset='utf8mb4',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    self.cursor = self.db.cursor()

#Exercici 1 
def afegeixGrup(meuID, nomGrup, altresUsuaris):
    self.conecta()
    
    sql = "INSERT INTO GRUPOS (nombre) VALUES (%s)"
    self.cursor.execute(sql, (nomGrup))
    sql = "SELECT MAX(id) FROM grups;"
    idGrup = self.cursor.execute(sql)
    sql = "INSERT INTO Rel_Usuarios_grupos(id_user, id_grup, administrador) VALUES (%s, %s, %s)"
    self.cursor.execute(sql, (meuID, idGrup, "SI"))
    for usuario in altresUsuaris:
        sql ="INSERT INTO Rel_Usuarios_Grupos (id_user, id_grup, administrador) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (usuario, idGrup, "No"))
    self.desconecta()
   
#Exercici 2.1 - Parte Base de Datos
def lletgirUsuaris(idGrup):
    self.conecta()
    
    sql = "SELECT u.id_user, u.nombre, r.administrador from Rel_Usuarios_grupos r, usuaris u WHERE r.id_usuario = u.id_usuario AND r.id_grup = %s "
    self.cursor.execute(sql (idGrup))
    
    self.desconecta()
    

#Exercici 2.2 - Parte EndPoint
@app.route('LlistaGrup/<id_grup>')
def llistaGrup(id_grup):
    usuaris = lletgirUsuaris(id_grup)
    return render_template('llistagrups.html', usuaris=usuaris)



