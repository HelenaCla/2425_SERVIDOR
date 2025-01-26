from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from jwt import PyJWTError
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt 

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Modelos Pydantic
class UserLogin(BaseModel):
    username: str
    password: str
    permits: str

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
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
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

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/login", response_model=Token)
def login(user: UserLogin):

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

@app.get("/equips")
def get_equipos():
    try:
        equipos = get_all_equipos()
        return equipos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resultats/equip/{id_equip}")
def get_resultats_equip(id_equip: int):
    try:
        resultats = get_resultats_por_equipo(id_equip)
        data = []
        for row in resultats:
            data.append({
                "local": row["HomeName"],
                "visitant": row["AwayName"],
                "resultat": f'{row["HomeGoals"]}-{row["AwayGoals"]}'
            })
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Resultado(BaseModel):
    Jornada: int
    fecha: str
    HomeTeam: int
    AwayTeam: int
    HomeGoals: int
    AwayGoals: int

@app.post("/resultats")
def add_resultado(resultado: Resultado):
    try:
        if check_match_exists(resultado.HomeTeam, resultado.AwayTeam):
            return {"message": "El partido ya existe en la base de datos"}
        insert_resultado(
            jornada=resultado.Jornada,
            fecha=resultado.fecha,
            home_team=resultado.HomeTeam,
            away_team=resultado.AwayTeam,
            home_goals=resultado.HomeGoals,
            away_goals=resultado.AwayGoals
        )
        return {"message": "Resultado insertado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/classificacio")
def get_classificacio():
    try:
        rows = get_classification_query()
        pos = 1
        for row in rows:
            row["posició"] = pos
            pos += 1
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            if (resultado.HomeTeam != code) or (resultado.AwayTeam != code):
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
