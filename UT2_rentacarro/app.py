from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import os
import json
from database import carrosdb

app = Flask(__name__)
app.config["SECRET_KEY"] = "millave"

@app.route('/')
@app.route('/llistacarros')
def carros():
    db = carrosdb()
    carros = db.cargarCarros()
    return render_template('carros.html', carros=carros)

@app.route("/Reservauncarro", methods=["GET", "POST"])
def carros2():
    db = carrosdb()
    carros = db.cargarCarros()  # Load carros list to pass to the template

    if request.method == "POST":
        nom = request.form['nom']
        llinatges = request.form['llinatges']
        diareserva = request.form['diareserva']
        horareserva = request.form['horareserva']
        diaretorno = request.form['diaretorno']
        horaretorno = request.form['horaretorno']
        carroreserva = request.form['carroreserva']
        usuario = f"{nom} {llinatges}"

        # Convertir las fechas y horas a objetos datetime
        iniciReserva = datetime.strptime(f"{diareserva} {horareserva}", "%d-%m-%Y %H")
        finalReserva = datetime.strptime(f"{diaretorno} {horaretorno}", "%d-%m-%Y %H")

        # Insertar la reserva en la base de datos
        db.insertarReserva(carroreserva, iniciReserva, finalReserva, usuario)

        return redirect(url_for('carros'))

    return render_template("carros2.html", carros=carros)

@app.route('/llistareservas')
def carros3():
    db = carrosdb()
    reservasPorCarro = db.verReservas()
    return render_template("carros3.html", reservasPorCarro=reservasPorCarro)

@app.route('/eliminaCarro')
def elimina():
    db = carrosdb()
    carros = db.cargarCarros()
    id=request.args.get('id')
    db.eliminaCarro(id)
    return render_template('carros4', carros=carros, id=id)


@app.route('/intranet-carros')
def carros4():
    db = carrosdb()
    carros = db.cargarCarros()
    return render_template('carros4.html', carros=carros)

if __name__ == '__main__':
    app.run(debug=True)
