from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

service = get_calendar_service()

app = Flask(__name__)

# Esta lista se sobreescribirá con los eventos del calendario.
lista = []

@app.route("/", methods=["GET", "POST"])
def tareas():
    global lista
    if request.method == "POST":
        asignatura = request.form.get("asignatura")
        tarea = request.form.get("tarea")
        fecha_hora = request.form.get("fecha_hora")
        print(fecha_hora)

        if asignatura and tarea and fecha_hora:
            fecha_hora_formateada = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M")

            # Añadimos la tarea a la lista local
            for item in lista:
                if item['asignatura'] == asignatura:
                    item['tareas'].append({"datetime": fecha_hora_formateada, "tarea": tarea})
                    break
            else:
                lista.append({'asignatura': asignatura, 'tareas': [{"datetime": fecha_hora_formateada, "tarea": tarea}]})

            # Reordenar las tareas por fecha
            for item in lista:
                item['tareas'] = sorted(item['tareas'], key=lambda x: datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M"))

            # Crear evento en Google Calendar
            start_datetime = datetime.strptime(fecha_hora_formateada, "%Y-%m-%d %H:%M")
            end_datetime = start_datetime + timedelta(hours=1)  # Duración del evento 1h

            event = {
                'summary': f"{asignatura}: {tarea}",
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'Europe/Madrid'
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'Europe/Madrid'
                }
            }

            created_event = service.events().insert(calendarId='primary', body=event).execute()
            print("Evento creado: {}".format(created_event.get('htmlLink')))

        return redirect(url_for("tareas"))

    # Si es GET, cargamos los eventos de Google Calendar en la lista
    # Limpia la lista antes de volver a cargar
    lista = []

    now = datetime.utcnow().isoformat() + 'Z'  # Momento actual en UTC con Z
    events_result = service.events().list(
        calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'Sin título')

        # Parsear asignatura y tarea del summary
        parts = summary.split(':', 1)
        if len(parts) == 2:
            asignatura_ev, tarea_ev = parts[0].strip(), parts[1].strip()
        else:
            # Si no cumple el formato "ASIGNATURA: Tarea", lo metemos en general
            asignatura_ev = "General"
            tarea_ev = summary

        # Convertir fecha
        # Quitar la 'Z' si la tiene, ya que datetime.fromisoformat no la soporta directamente
        start_clean = start.replace('Z', '')
        start_dt = datetime.fromisoformat(start_clean)
        fecha_hora_formateada = start_dt.strftime("%Y-%m-%d %H:%M")

        # Insertar en la lista
        for item in lista:
            if item['asignatura'] == asignatura_ev:
                item['tareas'].append({"datetime": fecha_hora_formateada, "tarea": tarea_ev})
                break
        else:
            lista.append({'asignatura': asignatura_ev, 'tareas': [{"datetime": fecha_hora_formateada, "tarea": tarea_ev}]})

    # Ordenar las tareas de cada asignatura por fecha
    for item in lista:
        item['tareas'] = sorted(item['tareas'], key=lambda x: datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M"))

    return render_template("tareas.html", lista=lista)

if __name__ == "__main__":
    app.run(debug=True)
