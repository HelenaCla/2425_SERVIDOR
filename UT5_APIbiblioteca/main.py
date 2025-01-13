from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Annotated
import database

app = FastAPI()
mt=database.biblioteca()

class Editor(BaseModel):
    NOM_EDIT: str
    ADR_EDIT: str
    CP_EDIT: str
    POB_EDIT: str
    TEL_EDIT: str
    FAX_EDIT: str
    EMAIL_EDIT: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the home page!"}

@app.get("/llibres/{id_llibre}")
def read_llibres(id_llibre):
    mt.conecta()
    result=mt.cargaLlibreid(id_llibre)
    mt.desconecta()
    return result

@app.get("/llibres/autor/{id_autor}")
def read_llibres_autor(id_autor):
    mt.conecta()
    result=mt.cargaLlibreAutor(id_autor)
    mt.desconecta()
    return result

@app.get("/editors")
def read_editors():
    mt.conecta()
    result=mt.cargaEditoresAll()
    mt.desconecta()        
    return result

@app.post("/editors")
async def escriu_editors(editor:Editor):
    print(editor.NOM_EDIT)
    mt.conecta()
    result=mt.nouEditor(editor.NOM_EDIT)
    mt.desconecta() 
    return result

@app.get("/editors/{id_editor}")
def read_editor_concret(id_editor):
    mt.conecta()
    result=mt.cargaEditor(id_editor)
    mt.desconecta()        
    return result

@app.put("/editors/{id_editor}")
def modifica_editor_concret(id_editor,editor:Editor):
    mt.conecta()
    result=mt.modificaEditor(id_editor,editor.NOM_EDIT)
    mt.desconecta()        
    return result

@app.delete("/editors/{id_editor}")
def esborra_editor(id_editor):
    mt.conecta()
    result=mt.esborraEditor(id_editor)
    mt.desconecta()        
    return result