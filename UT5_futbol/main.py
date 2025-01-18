from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import jwt
from jwt import PyJWTError
from typing import Optional
from datetime import datetime, timedelta

from database import (
    get_user_by_credentials,
    check_match_exists,
    insert_resultado
)

# Clave y algoritmo para firmar los JWT
SECRET_KEY = "mysecretkey"  # En producción, usar variable de entorno
ALGORITHM = "HS256"

# Tiempo que durará activo el token (ej. 30 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Modelos Pydantic
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Resultado(BaseModel):
    Jornada: int
    fecha: str
    HomeTeam: int
    AwayTeam: int
    HomeGoals: int
    AwayGoals: int

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Genera un JWT con los datos de 'data' y un tiempo de expiración.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """
    Decodifica el token JWT y retorna el payload si es válido.
    Si falla, retorna None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None

def get_current_user(authorization: str = ""):
    """
    Lógica para extraer el token de la cabecera 'Authorization: Bearer <token>'
    y validarlo. Si algo falla, lanza HTTP 401.
    Retorna el payload (dict) del token si es válido.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing or invalid format")

    token_str = authorization.split(" ")[1]
    payload = decode_token(token_str)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

    return payload

@app.post("/login", response_model=Token)
def login(user: UserLogin):
    """
    Endpoint para loguearse. 
    Recibe { username, password } y comprueba la BD.
    Si es correcto, genera un JWT con user_id, username, code.
    Retorna { access_token, token_type="bearer" }.
    """
    db_user = get_user_by_credentials(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Credencials invàlides")

    # Generamos el payload con la info del usuario
    payload = {
        "user_id": db_user["id"],
        "username": db_user["username"],
        "code": db_user["code"]
    }

    # Creamos el token con fecha de expiración
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_jwt = create_access_token(
        data=payload,
        expires_delta=access_token_expires
    )

    return {
        "access_token": token_jwt,
        "token_type": "bearer"
    }

@app.post("/resultats")
def add_resultado(resultado: Resultado, current_user: dict = Depends(get_current_user)):
    """
    Endpoint para insertar un nuevo partido en la BD, validado por JWT.
    - Solo si code == 99, puede insertar cualquier partido.
    - Si code está entre 0..19, solo puede insertar si uno de los equipos coincide con su code.
    - Si el partido ya existe, avisa.
    - Si otro error, da un 500.
    """
    try:
        code = current_user["code"]

        if code != 99:
            if (resultado.HomeTeam != code) and (resultado.AwayTeam != code):
                return {"message": "Aquest usuari no pot insertar un partit d'aquests equips."}

        if check_match_exists(resultado.HomeTeam, resultado.AwayTeam):
            return {"message": "El partit ja existeix a la base de dades"}

        insert_resultado(
            jornada=resultado.Jornada,
            fecha=resultado.fecha,
            home_team=resultado.HomeTeam,
            away_team=resultado.AwayTeam,
            home_goals=resultado.HomeGoals,
            away_goals=resultado.AwayGoals
        )
        return {"message": "Partit afegit correctament"}

    except Exception:
        raise HTTPException(status_code=500, detail="Error en la inserció del partit")
