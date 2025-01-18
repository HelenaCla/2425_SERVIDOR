from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import database, jwt_auth_users

app = FastAPI()
db = database.futbol()

# Modelos de datos para los resultados
class Resultado(BaseModel):
    home_team: int
    away_team: int
    home_goals: int
    away_goals: int
    jornada: int
    fecha: str

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Welcome to the home page!"}

# Ruta para obtener todos los equipos
@app.get("/equipos")
def read_equipos():
    db.conecta()
    result = db.cargaEquipos()
    db.desconecta()
    return result

# Ruta para obtener los resultados de un equipo específico
@app.get("/resultados/equipo/{id_equipo}")
def read_resultadoEquipo(id_equipo: int):
    db.conecta()
    result = db.cargaResultadosEquipo(id_equipo)
    db.desconecta()
    return result

# Ruta para agregar un resultado (partido) a la base de datos
@app.post("/resultados")
def create_resultado(result: Resultado, username: str = Depends(jwt_auth_users.get_current_user)):
    # Obtener el código de equipo del usuario actual
    user_team_code = jwt_auth_users.get_user_team_code(username)
    if user_team_code is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verificar si el usuario tiene permisos para insertar el partido
    if not is_valid_team_for_user(user_team_code, result.home_team, result.away_team):
        raise HTTPException(status_code=403, detail="Este usuario no puede insertar un partido de estos equipos.")
    
    db.conecta()
    response = db.añadirResultado(result.home_team, result.away_team, result.home_goals, result.away_goals, result.jornada, result.fecha)
    db.desconecta()
    return response

# Función que valida si un usuario tiene permiso para agregar un partido
def is_valid_team_for_user(user_team_code: int, home_team: int, away_team: int):
    # Si el código de equipo es 99, el usuario puede insertar cualquier partido
    if user_team_code == 99:
        return True
    # Si el código de equipo es entre 0 y 19, el usuario solo puede insertar partidos de su propio equipo
    return home_team == user_team_code or away_team == user_team_code

# Ruta para obtener la clasificación de los equipos
@app.get("/clasificacion")
def get_clasificacion():
    try:
        db.conecta()
        rows = db.clasificacion()
        pos = 1
        for row in rows:
            row['posició'] = pos
            pos += 1
        db.desconecta()
        return rows
    except Exception as e:
        db.desconecta()
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para el login y generación de token JWT
@app.post("/token")
def login(user: jwt_auth_users.User):
    authenticated_user = jwt_auth_users.authenticate_user(user.username, user.password)
    if authenticated_user is None:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    token = jwt_auth_users.create_access_token(data={"sub": authenticated_user["username"]})
    return {"access_token": token, "token_type": "bearer"}

