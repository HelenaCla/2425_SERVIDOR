from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField)
from wtforms.validators import DataRequired,ValidationError


app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'

# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
def check_usernames(form, field):
    if len(field.data) < 5:
        raise ValidationError('Ha de tenir més de 5 caracters')
    excluded_chars = " *?!'^+%&/()=}][{$#"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"El caràcter {char} no és vàlid.")

class InfoForm(FlaskForm):
    usuari = StringField('Tria el teu username',validators=[DataRequired(),check_usernames])
    submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        session['usuari'] = form.usuari.data
        return redirect(url_for("thankyou"))
    return render_template('02-home.html', form=form)


@app.route('/thankyou')
def thankyou():

    return render_template('02-thankyou.html')


if __name__ == '__main__':
    app.run(debug=True)
