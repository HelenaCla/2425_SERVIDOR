from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, get_flashed_messages
from pymysql.err import IntegrityError # type: ignore
from datetime import datetime, timedelta
from UT2_rentacarro.validations import validate_form
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
        iniciReserva = datetime.strptime(f"{diareserva} {horareserva}", "%d-%m-%Y %H:%M")
        finalReserva = datetime.strptime(f"{diaretorno} {horaretorno}", "%d-%m-%Y %H:%M")

        # Comprobar disponibilidad
        if not db.comprDispo(carroreserva, iniciReserva, finalReserva):
            flash('El carro ya está reservado en el intervalo de tiempo seleccionado.', 'error')
            return redirect(url_for('carros2'))
        
        # Calcular el costo
        coste = db.calculaCost(carroreserva, iniciReserva, finalReserva)
        
        try:
            # Insertar la reserva en la base de datos
            db.insertarReserva(carroreserva, iniciReserva, finalReserva, usuario)
            flash(f'Reserva realizada con éxito. El coste de la reserva es {coste}€. ', 'success')
        except IntegrityError:
            flash('Hubo un error al realizar la reserva. Por favor, inténtelo de nuevo.', 'error')
            return redirect(url_for('carros2'))
        return redirect(url_for('carros2'))

    return render_template("carros2.html", carros=carros)

@app.route('/llistareservas')
def carros3():
    db = carrosdb()
    # Obtener parámetros de fecha desde la URL, o usar el día de hoy como predeterminado
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date or not end_date:
        today = datetime.today()
        start_date = today.strftime('%Y-%m-%d')
        end_date = (today + timedelta(days=6)).strftime('%Y-%m-%d')
    reservas = db.mostraReserves(start_date, end_date)
    # Organizar reservas por carro y fechas
    reservas_dict = {}
    reservas_detalles = []
    dates_range = [(datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1)]
    for reserva in reservas:
        carro = reserva['nombreCarro']
        if carro not in reservas_dict:
            reservas_dict[carro] = {fecha: '' for fecha in dates_range}
        fecha = reserva['iniciReserva'].strftime('%Y-%m-%d')
        if fecha in reservas_dict[carro]:
            reservas_dict[carro][fecha] = reserva['usuario']
        
        # Calculando el coste de la reserva
        idcarro = reserva['idcarro']
        iniciReserva = reserva['iniciReserva']
        finalReserva = reserva['finalReserva']
        coste = db.calculaCost(idcarro, iniciReserva, finalReserva)
        
        # Guardamos los detalles
        reservas_detalles.append({
            'usuario': reserva['usuario'],
            'iniciReserva': iniciReserva,
            'finalReserva': finalReserva,
            'coste': coste
        })
    return render_template("carros3.html", reservas=reservas_dict, reservas_detalles=reservas_detalles, start_date=start_date, end_date=end_date, dates_range=dates_range, datetime=datetime, timedelta=timedelta)

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

@app.route('/crear-carro', methods=['GET', 'POST'])
def crearCarro():
    db = carrosdb()

    if request.method == 'POST':
        try:
            nombre = request.form['nom']
            descripcion = request.form['descripcio']
            clase = request.form['clase']
            preu = request.form['preu']
            img = request.form['img']

            db.crearCarro(nombre, descripcion, clase, preu, img)

            return redirect(url_for('carros4'))

        except KeyError as e:
            return f"Error: el campo {e} no se ha recibido correctamente."
    
    return render_template('creaCarro.html')


@app.route('/editar-carro/<int:id>', methods=['GET', 'POST'])
def editarCarro(id):
    db = carrosdb()
    if request.method == 'POST':
        nombre = request.form['nom']
        descripcion = request.form['descripcio']
        clase = request.form['clase']
        preu = request.form['preu']
        img = request.form['img']

        db.modificaCarro(id, nombre, descripcion, clase, preu, img)
        return redirect(url_for('carros4'))

    carro = db.mostraCarroPerId(id)
    return render_template('editCarros.html', carro=carro)

@app.route('/eliminar-carro/<int:id>')
def eliminarCarro(id):
    db = carrosdb()
    db.eliminaCarro(id)
    return redirect(url_for('carros4'))

@app.route('/registre')
def form():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def submit_form():
    # Recoger datos del formulario
    form_data = request.form.to_dict()

    # Validar los datos
    errors = validate_form(form_data)

    if errors:
        # Enviar errores como respuesta (puedes personalizar la presentación)
        return jsonify({"status": "error", "errors": errors}), 400

    # Si no hay errores, procesar el envío
    # Aquí podrías guardar los datos en una base de datos, enviar un email, etc.
    return jsonify({"status": "success", "message": "Formulario enviado correctamente"}), 200


if __name__ == '__main__':
    app.run(debug=True)
