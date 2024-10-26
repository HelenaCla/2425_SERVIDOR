from flask import Flask, render_template, request, session, redirect, url_for
import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


def TaulaAva(Llistareserves,carros,diaIni): #diaIni ve en format datetime
	#defino els dies
	dies=[]
	for dia in range(5):
		dies.append((diaIni+datetime.timedelta(days=dia)).strftime("%d-%m-%Y"))
	#faig una taula "pintar" buida (amb tots els carros i 5 dies buits "" )
	pintar=[]
	for carro in carros:
		pintar.append([carro['nom'],"","","","",""])
	#recorro la llista de reserves i modifico la taula "pintar" pel dia i carro concret
	for r in Llistareserves:
		for fila in pintar:
			if r['carro']==fila[0]:
				for columna in range(5):
					if r['dia']==dies[columna]:
						fila[columna+1]=r['usuari']
	return dies,pintar

def ComprovaReserva(nova,llista):
	for existents in llista:
		if existents['carro']==nova['carro'] and existents['dia']==nova['dia']:
			return False #Si retronam False es que JA EXISTIA RESERVA
	return True #si retornam True es que no hi ha coincidencia, la nova reserva es bona

@app.route('/')
@app.route('/llista')
def llista():
	#carregam els carros del fitxer json
	carrosList=json.load(open('./static/carros.json'))
	for c in carrosList:
		c['img']="../static/"+c['img']
	session['carros']=carrosList
	return render_template('carros.html',carros=carrosList)

@app.route('/reservar')
def reservar():
	carrosList=session['carros']
	return render_template('carros2.html',carros=carrosList)

# This page will have the sign up form
@app.route('/reserves')
def reserves():
	carrosList=session['carros']
	if session.get('llistareserves'):
		llistaReserves=session['llistareserves']
	else:
		llistaReserves=[]
	dies,pintar=TaulaAva(llistaReserves,carrosList,datetime.datetime.now())
	return render_template('carros3.html',reserves=llistaReserves,taulaAv=pintar,dies=dies)

# This page will have the sign up form
@app.route('/gestionaReserva')
def gestionaReserva():
	nuevaReserva={"usuari":request.args.get('nom')+" "+request.args.get('llinatge'),
				 "carro":request.args.get("carro"),
				 "dia":request.args.get('data')}
	if session.get('llistareserves'):
		llistaReserves=session['llistareserves']
	else:
		llistaReserves=[]
	if ComprovaReserva(nuevaReserva,llistaReserves):
		llistaReserves.append(nuevaReserva)
		session['llistareserves']=llistaReserves
		return redirect('/reserves')
	else:
		carrosList=session['carros']
		return render_template('carros2.html',carros=carrosList,alerta="Ya tenim reserva")

if __name__ == '__main__':
	app.run(debug=True)
