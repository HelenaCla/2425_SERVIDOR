from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import datetime
import urllib.request, json

app = Flask(__name__)

carrosList = []

@app.route('/')
@app.route('/llista')
def llista():
    global carrosList
    # Carreguem els carros del fitxer json
    carrosList = json.load(open('./static/carros.json'))
    for c in carrosList:
        c['img'] = "../static/" + c['img']
    return render_template('carros.html', carros=carrosList)

@app.route('/reservar')
def reservar():
    global carrosList
    return render_template('carros2.html', carros=carrosList)

# This page will have the sign up form
@app.route('/reserves')
def reserves():
    # Cargar los carros desde el archivo JSON
    carrosList = json.load(open('./static/carros.json'))

    # Generar las próximas 5 fechas
    today = datetime.date.today()
    next_5_days = [(today + datetime.timedelta(days=i +1)).strftime("%d-%m-%Y") for i in range(5)]

    # Pasar las fechas y la lista de carros al template
    return render_template('carros3.html', dates=next_5_days, carros=carrosList)

if __name__ == '__main__':
    app.run(debug=True)