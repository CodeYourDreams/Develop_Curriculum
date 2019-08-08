from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username: ')
    submit = SubmitField('Login!')

class MessageForm(FlaskForm):
    recipient = StringField(u"Recipient: ", validators=[DataRequired()])
    body = TextAreaField(u'Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class PostForm(FlaskForm):
    post = TextAreaField('Say something')
    submit = SubmitField('Submit')
