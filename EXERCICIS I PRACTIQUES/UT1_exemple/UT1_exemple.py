from flask import Flask, render_template
import datetime #heu de treure l'hora del servidor a partir d'aquesta llibreria
app = Flask(__name__)

@app.route('/')
def index():
    # Definim les variables
    nomUsuari="Helena"
    horaServidor=datetime.datetime.now()  
    horaformat=horaServidor.strftime("%H:%M %p")  
    # Passam les variables al template "index.html" que esta a la carpeta 'templates'
    return render_template('index.html',nom=nomUsuari,hora=horaformat)

if __name__ == '__main__':
    app.run(debug=True)
