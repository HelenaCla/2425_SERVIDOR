from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from database import Football
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
    db = Football()
    try:
        db.conecta()
        yield db
    finally:
        db.desconecta()

class Equipo(BaseModel):
    id: int  # Primary key, required
    equipo: Optional[str] = None  # Nullable column

class Result(BaseModel):
    Jornada: Optional[int] = None  # Nullable column
    Fecha: Optional[date] = None  # Nullable column
    HomeTeam: int  # Foreign key, required
    AwayTeam: int  # Foreign key, required
    HomeGoals: Optional[int] = None  # Nullable column
    AwayGoals: Optional[int] = None  # Nullable column

class User(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    permits: Optional[int] = None  # Nullable column

# Modelo de token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str


# User verification using the database
def authenticate_user(db: Football, username: str, password: str):
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
async def get_current_user(token: str = Depends(oauth2_scheme), db: Football = Depends(get_db)):
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
async def login(user: User, db: Football = Depends(get_db)):
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

# Welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the home page!"}

# Get info all teams
@app.get("/equips")
def read_equips(db: Football = Depends(get_db)):
    return db.cargaEquipsAll()

# Get results by team
@app.get("/resultats/equip/{id_equip}")
def read_resultats_equip(id_equip: int, db: Football = Depends(get_db)):
    resultats = db.cargaResultatsEquip(id_equip)
    if not resultats:
        raise HTTPException(status_code=404, detail="No results found for this team")
    return resultats

# Add a new result (depending on the user permits)
@app.post("/resultats")
def create_result(resultat: Result, db: Football = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user['permits'] != 99 and current_user['permits'] not in (resultat.HomeTeam, resultat.AwayTeam):
        raise HTTPException(status_code=401, detail="Aquest usuari no pot insertar un partit d'aquests equips.")
    new_res = db.nouResultat(resultat)
    if not new_res:
        raise HTTPException(status_code=404, detail="Error en la inserció del partit")
    return "Partit afegit correctament"

# Get the classification
@app.get("/classificacio")
def get_classificacio(db: Football = Depends(get_db)):
    classificacio = db.get_classificacio()
    if not classificacio:
        raise HTTPException(status_code=404, detail="No classification data found")
    return classificacio