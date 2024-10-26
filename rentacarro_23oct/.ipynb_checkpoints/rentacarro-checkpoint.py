from flask import Flask, render_template, request, session, redirect, url_for
import numpy as np
import datetime
import urllib.request, json

app = Flask(__name__)

carrosList=[]

@app.route('/')
@app.route('/llista')
def llista():
	global carrosList
	#carregam els carros del fitxer json
	carrosList=json.load(open('./static/carros.json'))
	for c in carrosList:
		c['img']="../static/"+c['img']
	return render_template('carros.html',carros=carrosList)

@app.route('/reservar')
def reservar():
	global carrosList
	return render_template('carros2.html',carros=carrosList)

# This page will have the sign up form
@app.route('/reserves')
def reserves():
	return render_template('carros3.html')

if __name__ == '__main__':
	app.run(debug=True)
