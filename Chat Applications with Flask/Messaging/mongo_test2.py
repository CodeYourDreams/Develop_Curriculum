import os, datetime
from chat_forms import LoginForm, MessageForm, RecipientForm
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_migrate import Migrate
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, \
AnonymousUserMixin, fresh_login_required
from flask_bootstrap import Bootstrap

from mongoengine import *
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc' # encrypts messages

#################################
###  DATABASE SECTION ###########
###################################

basedir = os.path.abspath(os.path.dirname(__file__))
 #app.config['POSTS_PER_PAGE'] = 30

client = pymongo.MongoClient("mongodb+srv://apouba:Codeyourdreams@cluster0-x2fzi.mongodb.net/test")
# client = pymongo.MongoClient("mongodb+srv://apouba:Codeyourdreams@cluster0-x2fzi.mongodb.net/test?retryWrites=true&w=majority")
# mongodb+srv://<username>:<password>@cluster0-x2fzi.mongodb.net/test

db = client.ChatInfo
messages = db.messages # collection
users = db.user # collection

Migrate(app, db)
login = LoginManager()
login.init_app(app)
bootstrap = Bootstrap(app)

connect('Project0')
##########################
### MODELS#################
#####################


users = {
    '_id' : ObjectId(),
    'username' : 'Guest',
    'last_seen' : datetime.datetime.now(),
    'messages_sent' : [{}, ...],
    'messages_received' : [{}, ...],
    'last_message_read_time' : datetime.datetime.now()
}

messages = {
    '_id' : ObjectId(),
    'author' : 'Guest',
    'recipient' : 'Guest',
    'body' : 'BODY',
    'timestamp' : datetime.datetime.now()
}


class Message(EmbeddedDocument): # mongoengine
    author = StringField()
    recipient = StringField()
    body = StringField()
    timestamp = DateTimeField(default = datetime.datetime.now())

    meta = {'allow_inheritance' : True}

    def __repr__(self):
        return '<Message {}>'.format(self.body)

#MongoEngine is a Document-Object Mapper (think ORM, but for
# document databases) for working with MongoDB from Python.
# It uses a simple declarative API, similar to the Django ORM.


class User(Document, UserMixin, AnonymousUserMixin):
    username = StringField(max_length = 25, Primary=True)
    id = IntField(default = 0)
    last_seen = DateTimeField(default = datetime.datetime.now())
    last_message_read_time = DateTimeField(default = datetime.datetime.now())
    messages_sent = EmbeddedDocumentField(Message)
    messages_received = EmbeddedDocumentField(Message)
    # image_file = StringField(default="default.jpg" maybe for profile

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(username):
    u = db.users.find_one({"username" : username})
    if not u:
        return None
    return User(username = u['username'])


############################
####### ROUTES ############
###########################

@app.route( '/' ) # home page
def index():
  return render_template( './chat_site_home.html' ) # using html file for this page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.users.find_one({'username': form.username.data})

        if user is None:
            user = {
                'username' : form.username.data,
                'last_seen' : datetime.datetime.now(),
                'messages_received' : None,
                'last_message_read_time' : datetime.datetime.now()
            }

            community = db.users.insert_one(user) # for mongoengine

        new_user = User(username=form.username.data) # for flask_login
        new_user.last_seen = datetime.datetime.now()
        new_user.last_message_read_time = datetime.datetime.now()
        new_user.save()
        login_user(new_user, force = True, fresh = True)

        return redirect(url_for('chat'))
    return render_template('cs_login.html', title='Sign In', form=form)


@app.route('/signup')
def signup():
    pass


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():

    form = RecipientForm()

    if form.validate_on_submit():
        user = current_user
        recipient = form.recipient.data
        return redirect(url_for('send', recipient = recipient))

    return render_template('phonebook.html', form=form)


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def send():

    recipient = request.args.get('recipient') # from form on last page
    form = MessageForm()

    if form.validate_on_submit():
        user = current_user
        msg = {
            'author' : user.username,
            'recipient' : recipient,
            'body' : form.body.data,
            'timestamp' : datetime.datetime.now()
        } # db
        chat = db.messages.insert_one(msg)
        community = db.users.insert_one(msg)

    # flask
    new_message = Message(author=current_user.username,
                            recipient=recipient,
                            body=form.body.data,
                            timestamp=datetime.datetime.now())

    # add msg to user's messages_sent & received
    sending = User(username = current_user.username,
                    messages_sent=new_message).save()
    recieving = User(username=recipient,
                    messages_received=new_message).save()

    flash(form.errors)

    page = request.args.get('page', 1, type=int)

    # showing messages from database dictionary
    received = db.messages.find({'recipient' : current_user.username,
                                'author' : recipient}).sort('timestamp')
    sent = db.messages.find({'author' : current_user.username,
                            'recipient' : recipient}).sort('timestamp')


    msgs = received, sent
    ############################################################
    # trying to combine these to render all sorted by timestamp
    # and not separated also by sent or received

    # msgs = (received, sent).sort('timestamp')
    # #msgs = received.update(sent)

    ####################################################################
    # These were from a blog template but may be helpful for certain apps

    # next_url = url_for('index', page=messages.next_num) \
    #     if messages.has_next else None
    # prev_url = url_for('login', page=messages.prev_num) \
    #     if messages.has_prev else None

    # maybe add profile picture or avatar
    img = user.image_file

    return render_template('messages.html', form=form, received=received,
                            sent=sent, recipient=recipient, msgs=msgs, img=img)
                           # next_url=next_url, prev_url=prev_url)


if __name__ == '__main__':
  app.run(debug = True) #opens debug traceback
  # and with debug pin from console, gives a debugging console
