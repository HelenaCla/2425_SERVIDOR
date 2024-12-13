from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Lista inicial de tareas
lista = [
    {'asignatura': 'DWES', 'tareas': [
        {"datetime": "2024-12-10 20:00", "tarea": "Examen 1 Av"},
        {"datetime": "2024-12-15 20:00", "tarea": "Entrega activitat rentacarro"}
    ]},
    {'asignatura': 'DWEC', 'tareas': [
        {"datetime": "2024-12-08 20:00", "tarea": "Examen"},
        {"datetime": "2024-12-11 19:00", "tarea": "Activitat 3"}
    ]}
]

@app.route("/", methods=["GET", "POST"])
def tareas():
    if request.method == "POST":
        asignatura = request.form.get("asignatura")
        tarea = request.form.get("tarea")
        fecha_hora = request.form.get("fecha_hora")
        print(fecha_hora)

        if asignatura and tarea and fecha_hora:
                           # Validar y convertir la fecha al formato esperado
            fecha_hora_formateada = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M")
                
                # Agregar la nueva tarea
            for item in lista:
                if item['asignatura'] == asignatura:
                    item['tareas'].append({"datetime": fecha_hora_formateada, "tarea": tarea})
            # Agregar la nueva tarea a la asignatura correspondiente

            else:
                # Si la asignatura no está en la lista, añadirla
                lista.append({'asignatura': asignatura, 'tareas': [{"datetime": fecha_hora_formateada, "tarea": tarea}]})

            # Reordenar las tareas por fecha
            for item in lista:
                item['tareas'] = sorted(item['tareas'], key=lambda x: datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M"))

        return redirect(url_for("tareas"))

    return render_template("tareas.html", lista=lista)

if __name__ == "__main__":
    app.run(debug=True)


