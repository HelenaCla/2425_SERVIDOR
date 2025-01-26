from flask import Flask, render_template, request
from database import Biblioteca
app = Flask(__name__)


@app.route('/')
def index():
	departaments=Biblioteca.cargaDepartaments()
	return render_template('template_base.html',departaments=departaments)

# This page will have the sign up form
@app.route('/llibres')
def llibres():
	dep = request.args.get('departament')
	departaments=Biblioteca.cargaDepartaments()
	llibres=Biblioteca.cargaLlibres(dep)	
	return render_template('llibres.html',departaments=departaments,llibres=llibres)

if __name__ == '__main__':
	app.run(debug=True)
