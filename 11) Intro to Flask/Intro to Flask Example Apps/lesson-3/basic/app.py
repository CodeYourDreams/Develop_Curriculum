# basic.py

# Add importing session and redirect from the earlier example
from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm

# The parentheses allow all the imports to be on seperate lines without error
from wtforms import (StringField, BooleanField, DateTimeField, RadioField,
                     SelectField, TextField, TextAreaField, SubmitField)

# Import DataRequired one of many possible form validators
from wtforms.validators import DataRequired


app = Flask(__name__)

# Set secret key to an arbitrary string
app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    # This is the first part of the form, a StringField, so users are presented with the question "What breed are you?" and then provide a string answer
    # DataRequired is used here as a validator, therefore it will make sure data is recieved for this question
    breed = StringField('What breed are you?', validators=[DataRequired()])

    # This is another form field, BooleanField, so the user is presented with the question, then can check the box for yes, or leave it unchecked for no (a checkbox)
    neutered = BooleanField("Have you been neutered?")

    # Another form field type, RadioField. For the choices, the first part, such as mood_one or mood_two, of each is for back_end
    # The second part, such as Happy or Excited, is what is presented to the user for each radio button, as the label
    mood = RadioField('Please choose your mood:', choices=[('mood_one', 'Happy'), ('mood_two', 'Excited')])

    # This works the same as the RadioField, but is presented in a different style than the radio buttons as a dropdown list
    food_choice = SelectField('Pick you favorite food:', choices=[('chi', 'Chicken'), ('bf', 'Beef'), ('fish', 'Fish')])

    # TextAreaField is for a user to write long-form (paragraph) text
    feedback = TextAreaField()

    # A SubmitField is a button for the user to submit the form
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        # This session dict is a way to store data for a specific amount of time, from when a user logs in to when they log out
        # Treat it like a dictionary, using 'breed' as a key
        session['breed'] = form.breed.data
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data

        # This redirection to the thankyou page only happens upon valid submission of the form
        return redirect(url_for('thankyou'))

    # Otherwise, return the index
    return render_template('home.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
