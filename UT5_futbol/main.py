from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_all_equipos, check_match_exists, insert_resultado, get_resultats_por_equipo, get_classification_query

app = FastAPI()

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
