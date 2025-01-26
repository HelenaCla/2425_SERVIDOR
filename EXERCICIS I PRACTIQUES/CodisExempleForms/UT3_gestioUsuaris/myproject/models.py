from myproject import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import pymysql.cursors

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(gugug):
    if gugug:
        user=User()
        user.fromID(gugug)
        print("estoy haciendo algo")
        print("el id es "+str(gugug))
        return user

class User(UserMixin):
    #id = 0

    def __init__(self):
        self.username = "null"

    def fromUsername(self, username):
        self.username = username
        RQ=self.getId()
        if RQ:
            #print(RQ)
            self.rol=RQ['rol']
            self.id=RQ['id']
            self.email=RQ['email']

    def fromID(self,Userid):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='usuarisut4',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        print(Userid)
        sql="SELECT id,email,rol,usuari from usuaris WHERE id="+str(Userid)
        print(sql)
        cursor.execute(sql)
        ResQuery=cursor.fetchone()
        if ResQuery:
            self.id=ResQuery['id']
            self.rol=ResQuery['rol']
            self.email=ResQuery['email']
            self.username=ResQuery['usuari']

    def comprovaUsuari(self,pwd):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='usuarisut4',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT count(*) from usuaris WHERE usuari='"+self.username+"'"
        cursor.execute(sql)
        ResQuery=cursor.fetchone()
        if ResQuery['count(*)']==1:
            sql="SELECT password from usuaris  WHERE usuari='"+self.username+"'"
            cursor.execute(sql)
            ResQuery=cursor.fetchone()
            resposta=check_password_hash(ResQuery['password'],pwd)
            self.getId()
        else:
            resposta=False
        db.close()
        return resposta

    def getId(self):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='usuarisut4',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT id,email,rol from usuaris WHERE usuari='"+self.username+"'"
        cursor.execute(sql)
        ResQuery=cursor.fetchone()
        if ResQuery:
            self.id=ResQuery['id']
            self.rol=ResQuery['rol']
            self.email=ResQuery['email']
            return ResQuery
        else:
            return False

    def getUsername(self):
        return self.username

    def nouUsuari(self,username,password,email):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='usuarisut4',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT max(id)+1 nouId from usuaris"
        cursor.execute(sql)
        ResQuery=cursor.fetchone()                        
        sql="INSERT into usuaris values("+str(ResQuery['nouId'])+",'"+username+"','"+generate_password_hash(password)
        sql=sql+"','"+email+"','user')"
        cursor.execute(sql)
        return ResQuery['nouId']

    def modificaUsuari(self,idusuari,email,password):
        #Conexion a la BBDD del servidor mySQL
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='usuarisut4',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="UPDATE usuaris SET password='"+generate_password_hash(password)+"', email='"+email+"' WHERE id="+str(idusuari)
        cursor.execute(sql)
       
