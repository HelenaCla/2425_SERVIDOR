from flask import Flask, render_template, request
import datetime
from database import vols


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/')
def index():
    aeroports=vols().cargaAeroports()
    return render_template('index.html', aeroports=aeroports)

@app.route('/vols/<codiAeroport>')
def volsAeroport(codiAeroport):
    vols_instance = vols()
    aeroports = vols_instance.cargaAeroports()
    
    arribades = vols_instance.cargaArribades(codiAeroport, datetime.datetime.now())
    sortides = vols_instance.cargaSortides(codiAeroport, datetime.datetime.now())
    
    arribadesNac = [vol for vol in arribades if vol['departure_country'] == vol['arrival_country']]
    arribadesInt = [vol for vol in arribades if vol['departure_country'] != vol['arrival_country']]
    sortidesNac = [vol for vol in sortides if vol['departure_country'] == vol['arrival_country']]
    sortidesInt = [vol for vol in sortides if vol['departure_country'] != vol['arrival_country']]
    
    return render_template('aeroport.html', codi=codiAeroport,
                           aeroports=aeroports,
                           arribadesNac=arribadesNac,
                           arribadesInt=arribadesInt,
                           sortidesNac=sortidesNac,
                           sortidesInt=sortidesInt)

@app.route('/delay_flight/<int:flight_id>', methods=['POST'])
def delay_flight(flight_id):
    vols().delayFlight(flight_id, hours=2)
    return redirect(request.referrer)

if __name__ == '__main__':
	app.run(debug=True)
