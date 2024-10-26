from flask import Flask, render_template, request, session
from datetime import datetime
import os
import json
app = Flask(__name__)
app.config["SECRET_KEY"]="millave"
lista=[]
fechas=[]

for i in range(5):
    fechas.append(datetime(datetime.now().year,datetime.now().month,datetime.now().day + i + 1).strftime("%d-%m-%Y"))

@app.route('/')
@app.route('/llistacarros')
def carros():
    json_path = os.path.join(app.static_folder, 'carros.json')
    with open(json_path) as file:
        carros = json.load(file)
    return render_template('carros.html', carros=carros)

@app.route('/Reservauncarro')
def carros2():
    json_path = os.path.join(app.static_folder, 'carros.json')
    with open(json_path) as file:
        carros = json.load(file)
    return render_template('carros2.html', carros=carros)

@app.route('/llistareservas')
def carros3():
    session["lista"]=lista
    reservasPorCarro = llenaCarros(lista, fechas)
    return render_template("carros3.html", lista=session["lista"], fechas=fechas, reservas=reservasPorCarro)


@app.route("/nuevareserva", methods=["POST"])
def nuevareserva():
    json_path = os.path.join(app.static_folder, 'carros.json')
    with open(json_path) as file:
        carros = json.load(file)
    data_reserva = request.form.get('data_reserva')
    # Validar la fecha de reserva
    today = datetime.now().date()
    try:
        data_reserva_date = datetime.strptime(data_reserva, "%d-%m-%Y").date()
        if data_reserva_date < today:
            error = "La fecha de la reserva ha de ser para hoy o posterior"
            return render_template('carros2.html',carros=carros, error=error)
    except ValueError:
        error = "Formato de fecha incorrecto. Utiliza dd-mm-yyyy."
        return render_template('carros2.html',carros=carros, error=error)

    #Session
    entrada={"nom":request.form.get("nom")+' '+request.form.get("llinatges"),"carro":request.form.get("carro"), "fecha":data_reserva}
    if not comprobarReserva(entrada, lista):
        lista.append(entrada)
        session["lista"]=lista
        reservasPorCarro = llenaCarros(lista, fechas)
        return render_template("carros3.html", lista=session["lista"], reserva='La reserva se ha efectuado correctamente', fechas=fechas, reservas=reservasPorCarro)
    # Si todo es correcto, redirigir a la lista de reservas
    return render_template("carros2.html", error='La reserva no se ha efectuado por duplicidad')

def comprobarReserva(prueba, lista):
    resultado = False
    for reserva in lista:
        if reserva["carro"]==prueba["carro"] and reserva["fecha"]==prueba["fecha"]:
            resultado = True
    return resultado

def llenaCarros(lista, fechas):
    reservasPorCarro = {}

    for reserva in lista:
        if reserva["fecha"] in fechas:
            if reserva["carro"] not in reservasPorCarro:
                reservasPorCarro[reserva["carro"]] = {fecha: None for fecha in fechas}
            reservasPorCarro[reserva["carro"]][reserva["fecha"]] = reserva["nom"]

    return reservasPorCarro


if __name__ == '__main__':
    app.run(host="192.168.48.134")