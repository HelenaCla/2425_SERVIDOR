from myproject import app
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user,current_user
from myproject.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    usuari= request.form['usuari']
    pwd=request.form['password']
    user=User()
    user.fromUsername(usuari)
    if user.comprovaUsuari(pwd):
        #user.getId()
        print(user)
        login_user(user)
        return redirect(url_for('welcome_user'))
    else:
        return render_template('login.html',loginmsg="Login Incorrecte")

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('main.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@app.route('/registerForm')
@login_required
def register_form():
    return render_template('register.html')

@app.route('/modifyForm')
@login_required
def modify_form():
    print(current_user.id)
    return render_template('modify.html')

@app.route('/register')
@login_required
def register():
    nom= request.args.get('nom')
    pwd= request.args.get('password')
    email= request.args.get('email')
    user=User()
    user.nouUsuari(nom,pwd,email)
    return redirect(url_for('welcome_user'))

@app.route('/modify')
@login_required
def modify():
    pwd= request.args.get('password')
    email= request.args.get('email')
    user=User()
    user.fromID(current_user.id)
    user.modificaUsuari(current_user.id,email,pwd)
    return redirect(url_for('welcome_user'))

if __name__ == '__main__':
    app.run(debug=True)
