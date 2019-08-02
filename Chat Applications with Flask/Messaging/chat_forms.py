from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, validators

class LoginForm(FlaskForm):
    username = StringField('Username: ')
    submit = SubmitField('Login!')

class MessageForm(FlaskForm):
    message = TextAreaField('Message')
    submit = SubmitField('Send')
