from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

import requests
# import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
pokemons=[{"nom":"drowzee","categoria":"hipnosis","tipo":"psiquico"},
		  {"nom":"blissey","categoria":"felicidad","tipo":"normal"},
		  {"nom":"munkidori","categoria":"esbirro","tipo":["veneno","psiquico"]},]


@app.route('/pokemon/<nomPokemon>')
def index(nomPokemon):
	for pokemon in pokemons:
		if pokemon['nom']== nomPokemon:
			return render_template('pokemon.html',pokemon=pokemon)
	return render_template('error.html')


@app.route('/api/<nomPokemon>')
def api(nomPokemon):
    r = requests.get('https://pokeapi.co/api/v2/pokemon/' + nomPokemon)
    try:
        datospokemon = r.json()
        
        location_url = datospokemon['location_area_encounters']
        location_response = requests.get(location_url).json()
        
        locations = [loc['location_area']['name'] for loc in location_response]
        
        return render_template('pokemon.html', pokemon=datospokemon, locations=locations)
    except:
        return render_template('error.html')


if __name__ == '__main__':
	app.run(debug=True)
