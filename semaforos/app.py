from flask import Flask, render_template, request, redirect, url_for, jsonify

# Inicializar la aplicación Flask
app = Flask(__name__)

# Simular la base de datos con un diccionario
traffic_lights = [
    {"id": 1, "name": "Semáforo 1", "status": "red"},
    {"id": 2, "name": "Semáforo 2", "status": "yellow"},
    {"id": 3, "name": "Semáforo 3", "status": "green"}
]

# Ruta principal para mostrar los semáforos y sus estados
@app.route('/')
def index():
    return render_template('index.html', lights=traffic_lights)

# Ruta para actualizar el estado de un semáforo
@app.route('/update/<int:light_id>/<string:status>', methods=['POST'])
def update(light_id, status):
    light = next((light for light in traffic_lights if light['id'] == light_id), None)
    if light:
        light['status'] = status
    return redirect(url_for('index'))

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
