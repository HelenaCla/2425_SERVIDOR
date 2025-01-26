from flask import Flask, render_template, flash,session, redirect, url_for, session
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired,Regexp


app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'

# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class InfoForm(FlaskForm):
    breed = StringField('What breed are you?',validators=[DataRequired()])
    neutered  = BooleanField("Have you been neutered?")
    mood = RadioField('Please choose your mood:', choices=[('mood_one','Happy'),('mood_two','Excited')])
    food_choice = SelectField(u'Pick Your Favorite Food:',
                          choices=[('chi', 'Chicken'), ('bf', 'Beef'),
                                   ('fish', 'Fish')])
    telephone=StringField('What are your telephone? [spanish number with 9 digits]',validators=[DataRequired(), Regexp('^[0-9]{9}$',message='El telefono debe ser de 9 cifras')])
    feedback = TextAreaField()
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()
    # If the form is valid on submission 
    if form.validate_on_submit():
        # Grab the data 
        session['breed'] = form.breed.data
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data
        session['telephone'] = form.telephone.data
        return redirect(url_for("thankyou"))
    return render_template('01-home.html', form=form)


@app.route('/thankyou')
def thankyou():
    return render_template('01-thankyou.html')


if __name__ == '__main__':
    app.run(debug=True)
