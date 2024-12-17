from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, get_flashed_messages
from pymysql.err import IntegrityError # type: ignore
from datetime import datetime, timedelta
from validations import validate_form
from database import carrosdb
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request
app = Flask(__name__)
app.config["SECRET_KEY"] = "millave"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, nom, llinatges):
        self.id = id
        self.username = username
        self.nom = nom
        self.llinatges = llinatges

@app.route('/')
@app.route('/llistacarros')
@login_required
def carros():
    db = carrosdb()
    carros = db.cargarCarros()
    return render_template('carros.html', carros=carros)

@app.route("/Reservauncarro", methods=["GET", "POST"])
@login_required
def carros2():
    db = carrosdb()
    carros = db.cargarCarros()  # Load carros list to pass to the template

    if request.method == "POST":
        diareserva = request.form['diareserva']
        horareserva = request.form['horareserva']
        diaretorno = request.form['diaretorno']
        horaretorno = request.form['horaretorno']
        carroreserva = request.form['carroreserva']
    
            # Construir el usuario a partir de current_user
        usuario = f"{current_user.nom} {current_user.llinatges}"
    
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
@login_required
def carros3():
    db = carrosdb()
    
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    # Si no se proporcionan start_date ni end_date
    if not start_date or not end_date:
        current_username = f"{current_user.nom} {current_user.llinatges}"
        next_res = db.next_user_reservation(current_username)
        
        if next_res:
            weekday = next_res.weekday() 
            monday = next_res - timedelta(days=weekday)
            start_dt = monday
            end_dt = monday + timedelta(days=6)
        else:
            today = datetime.today()
            start_dt = today
            end_dt = today + timedelta(days=6)
        
        start_date = start_dt.strftime('%Y-%m-%d')
        end_date = end_dt.strftime('%Y-%m-%d')
    
    # Resto de la lógica ya existente
    carros = db.cargarCarros()
    reservas = db.mostraReserves(start_date, end_date)

    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    days_count = (end_dt - start_dt).days + 1
    dates_range = [
        (start_dt + timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(days_count)
    ]

    reservas_dict = {}
    for carro in carros:
        reservas_dict[carro['nom']] = {fecha: "LIBRE" for fecha in dates_range}

    current_username = f"{current_user.nom} {current_user.llinatges}"

    for reserva in reservas:
        carro = reserva['nombreCarro']
        usuario_reserva = reserva['usuario']
        inici = reserva['iniciReserva']
        final = reserva['finalReserva']

        for fecha in dates_range:
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
            if inici.date() <= fecha_dt.date() <= final.date():
                if usuario_reserva == current_username:
                    reservas_dict[carro][fecha] = "RESERVADO"
                else:
                    reservas_dict[carro][fecha] = "NO DISPONIBLE"

    prev_start = (start_dt - timedelta(days=7)).strftime('%Y-%m-%d')
    prev_end = (start_dt - timedelta(days=1)).strftime('%Y-%m-%d')
    next_start = (end_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    next_end = (end_dt + timedelta(days=7)).strftime('%Y-%m-%d')

    return render_template("carros3.html",
                           reservas=reservas_dict,
                           start_date=start_date,
                           end_date=end_date,
                           dates_range=dates_range,
                           prev_start=prev_start,
                           prev_end=prev_end,
                           next_start=next_start,
                           next_end=next_end)



@app.route('/eliminaCarro')
@login_required
def elimina():
    db = carrosdb()
    carros = db.cargarCarros()
    id=request.args.get('id')
    db.eliminaCarro(id)
    return render_template('carros4', carros=carros, id=id)


@app.route('/intranet-carros')
@login_required
def carros4():
    db = carrosdb()
    carros = db.cargarCarros()
    return render_template('carros4.html', carros=carros)

@app.route('/crear-carro', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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


@login_manager.user_loader
def load_user(user_id):
    db = carrosdb()
    usuario = db.mostraUsuariPerId(user_id)
    if usuario:
        return User(id=usuario['id'], username=usuario['username'], nom=usuario['nom'], llinatges=usuario['llinatges'])
    return None

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = carrosdb()
        usuario = db.cargarUsuarioPorUsername(username)
        
        if usuario and check_password_hash(usuario['password_hash'], password):
            user = User(id=usuario['id'], username=usuario['username'], nom=usuario['nom'], llinatges=usuario['llinatges'])
            login_user(user)
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('carros'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))

from werkzeug.security import generate_password_hash

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        errors = validate_form(form_data)

        if errors:
            for err in errors:
                flash(err, 'error')
            return redirect(url_for('registro'))

        username = request.form['username']
        nom = request.form['nom']
        llinatges = request.form['llinatges']
        email = request.form['email']
        telefon = request.form['telefon']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        fecha_alta = datetime.now().date()
        
        if password != password_repeat:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('registro'))
        
        password_hash = generate_password_hash(password)
        
        db = carrosdb()
        try:
            db.crearUsuari(username, nom, llinatges, email, telefon, password_hash, fecha_alta)
            flash('Usuario registrado con éxito. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            flash('El usuario o el correo ya están registrados.', 'error')
    
    return render_template('registro.html')


@app.context_processor
def inject_request():
    return dict(request=request)

if __name__ == '__main__':
    app.run(debug=True)

