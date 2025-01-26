from flask import app, render_template

@app.route('/prova')
def index():
    usuari1=[{"nom":"Acceptar", "habilitat":"si"},
             {"nom":"Cancelar", "habilitat":"si"},
             {"nom":"Nou Usuari", "habilitat":"no"}]
    return render_template('main.html', botons=usuari1);
"""""
E
    M
        G L H
    M
    Ñ
        F L M
    Ñ
    A
E

{% for but in botons %}
    {% if but[‘habilitat’]==”si” %}
        <button> {{ but[‘nom’] }} </button>
    {% else %}
        <button disabled> {{ but[‘nom’] }} </button>    
    {% endif %}
    
""""