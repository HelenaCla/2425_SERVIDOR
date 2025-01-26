from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, field_validator
from database import Chat
from typing import Optional
from datetime import datetime, date, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt 


# Clave secreta para firmar los tokens (debería ser una variable de entorno en producción)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración para el esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Dependency to get a database instance
def get_db():
    db = Chat()
    try:
        db.conecta()
        yield db
    finally:
        db.desconecta()
        
session[i] = 0

class User(BaseModel):
    User_ID: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None

# Modelo de token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Modelo de mensaje
# ERAN 5 PROPIEDADES, NO RECUERDO LAS ULTIMAS 2
class Message(BaseModel):
    Message_ID: Optional[int] = None # ESTA NO SE SI ES NECESARIO
    Content: str
    Date: datetime = datetime.now() # Fecha de envío
    # EL ESTADO DE LOS MSJS LO PODEMOS PONER EN PLAN BOOLEANDO/ENUM DEL 0 AL 4, SIN ENVIAR, ENVIADO, RECIBIDO Y LEIDO 
    # SI TENEMOS "SIN ENVIAR" TENDRÍAMOS QUE TENER UN ALMACENAMIENTO LOCAL O LA OPCION ES QUE NO HAYA SIN ENVIAR Y 
    # EL MSJ DESAPAREZCA SI EL QUE LO ENVIA NO TIENE CONX
    Status: int = 1  # Foreign key, required
    Sender: str # Foreign key, required
    Receiver: str # Foreign key, required

    @field_validator("Content")
    def validate_content(cls, value):
        if not value.strip():
            raise ValueError("Message content cannot be empty.")
        return value
    
    
# Modelo de grupo
class Group(BaseModel):
    Group_ID: Optional[int] = None
    Name: str
    Description: Optional[str] = None
    Admin: str #No se si serán str para el uname o los users tendrán id, jose nos va a dar la bd, igual en principio el creador es admin
    Members: list[str]

# User verification using the database
def authenticate_user(db: Chat, username: str, password: str):
    try:
        user_data = db.checkUser(username)
        if user_data and user_data['password'] == password:  # Replace with password hashing if used
            return {
                "username": user_data['username'],
                "permits": user_data['permits']
            }
        return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None


# Create a JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Validate the JWT token and get the current user and permits
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        permits: str = payload.get("permits")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Fetch user details from the database
        user_data = {
            "username": username,
            "permits": permits
        }
        return user_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Endpoint to generate a token
@app.post("/token", response_model=Token)
async def login(user: User, db: Chat = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user["username"], "permits": authenticated_user["permits"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"message": "Welcome to the home page!"}


#ACA TODO LO QUE ES MENSAJERIA BASICA, ENVIAR, RECIBIR, CAMBIAR ESTADO.

# Endpoint to send a message
@app.post("/send")
def send_message(message: Message, db: Chat = Depends(get_db)):
    return db.sendMessage(message)

# Endpoint to check the number of messages the user has received and not read
@app.get("/check_messages")
def check_messages(db: Chat = Depends(get_db), receiver: str = Depends(get_current_user)):
    db.checkMessages(receiver)
    return RedirectResponse(url="/change_state/{2}", status_code=303)

# Endpoint to change the state of a message after the user has received it
@app.put("/change_state/{2}")#o change_state_recieved, no se
def change_state_recieved(db: Chat = Depends(get_db)):
    return db.changeMessageState(2)

# Endpoint to get all messages
@app.get("/recieve_messages") # ESTE TIENE QUE SER UN ONCLICK EN EL CHAT ESPECIFICO Y HAY QUE VER CÓMO CAMBIAR EL OFFSET AL HACER SCROLL (O PONERMOS BOTONES)
def recieve_messages(limit: int = 10, offset: int = i, db: Chat = Depends(get_db), receiver: str = Depends(get_current_user), sender: str = user_ID): #ARREGLAR
    i = cargarMensajesAnteriores()
    db.getMessages(limit=limit, offset=offset, sender=sender, receiver=receiver)
    return RedirectResponse(url="/change_state/{3}", status_code=303)

def cargarMensajesAnteriores():
    return i + 10

# Endpoint to change the state of a message after the user has read it
@app.put("/change_state/{3}")#o change_state_seen, no se
def change_state_recieved(db: Chat = Depends(get_db)):
    return db.changeMessageState(3)

# Endpoint to change the content of a message [ACÁ TENDRÍAMOS QUE PONER UN LIMITE DE TIEMPO O ASÍ]
@app.put("/change_content/{message_id}/{content}")
def change_content(message_id: int, content: str, db: Chat = Depends(get_db)):
    return db.changeContent(message_id, content)

# Endpoint to delete a message
@app.delete("/delete_message/{message_id}") # ESTE DEJA DE SER POSIBLE CUANDO EL ESTADO AMBIA A LEIDO (4)
def delete_message(message_id: int, db: Chat = Depends(get_db)):
    return db.deleteMessage(message_id)


#Acá todo lo de crear grupos y maybe administrar usuarios

# Endpoint to create a group
@app.post("/create_group")
def create_group(group: Group, db: Chat = Depends(get_db)):
    return db.createGroup(group)

# Endpoint to add a user to a group
@app.put("/add_user/{group_id}/{user_id}")
def add_user_to_group(group_id: int, user_id: int, db: Chat = Depends(get_db)):
    return db.addUserToGroup(group_id, user_id)

# Endpoint to delete a user from a group
@app.delete("/delete_user/{group_id}/{user_id}")
def delete_user_from_group(group_id: int, user_id: int, db: Chat = Depends(get_db)):
    return db.deleteUserFromGroup(group_id, user_id)

# Endpoint to delete a group
@app.delete("/delete_group/{group_id}")
def delete_group(group_id: int, db: Chat = Depends(get_db)):
    return db.deleteGroup(group_id)

# Endpoint to change group name
@app.put("/change_name/{group_id}/{name}")
def change_name(group_id: int, name: str, db: Chat = Depends(get_db)):
    return db.changeName(group_id, name)

# Endpoint to change group admin
@app.put("/change_admin/{group_id}/{user_id}")
def change_admin(group_id: int, user_id: int, db: Chat = Depends(get_db)):
    return db.changeAdmin(group_id, user_id)

# Endpoint to change group description
@app.put("/change_description/{group_id}/{description}")
def change_description(group_id: int, description: str, db: Chat = Depends(get_db)):
    return db.changeDescription(group_id, description)


# @app.get("/resultats/equip/{id_equip}")
# def read_resultats_equip(id_equip: int, db: Chat = Depends(get_db)):
#     resultats = db.cargaResultatsEquip(id_equip)
#     if not resultats:
#         raise HTTPException(status_code=404, detail="No results found for this team")
#     return resultats

