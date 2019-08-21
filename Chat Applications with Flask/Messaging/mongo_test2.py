import os, datetime, getpass
from chat_forms import LoginForm, MessageForm, PostForm
from flask import Flask, render_template, url_for, redirect, request, flash, current_app
from flask_sqlalchemy import SQLAlchemy
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
### SQL DATABASE SECTION ###########
###################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['POSTS_PER_PAGE'] = 30

client = pymongo.MongoClient("mongodb+srv://apouba:Codeyourdreams@cluster0-x2fzi.mongodb.net/test")
#client = pymongo.MongoClient("mongodb+srv://apouba:Codeyourdreams@cluster0-x2fzi.mongodb.net/test?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb+srv://apouba:Codeyourdreams@cluster0-x2fzi.mongodb.net/test?retryWrites=true&w=majority")
# mongodb+srv://apouba:<password>@cluster0-x2fzi.mongodb.net/test

db = client.ChatInfo
messages = db.messages # collection
users = db.user # collection


Migrate(app,db)
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


class Message(EmbeddedDocument): # DynamicDocument ? / Embedded ?
    author = StringField()
    recipient = StringField()
    body = StringField()
    timestamp = DateTimeField(default = datetime.datetime.now())

    # messages_sent = ListField(ReferenceField('User'))
    # messages_recieved = ListField(ReferenceField('User'))

    meta = {'allow_inheritance' : True}

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class MSent(Message):
    content = StringField()

class MRecieved(Message):
    content = StringField()


class User(Document, UserMixin, AnonymousUserMixin):
    username = StringField(max_length = 25, Primary=True)
    id = IntField(default = 0)
    # user_id = User.objects.count()
    last_seen = DateTimeField(default = datetime.datetime.now())
    last_message_read_time = DateTimeField(default = datetime.datetime.now())
    messages_sent = EmbeddedDocumentField(Message)
    messages_received = EmbeddedDocumentField(Message)

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
    #
    # def new_messages(self):
    #     last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
    #     return Message.query.filter_by(recipient=self).filter(
    #         Message.timestamp > last_read_time).count()

    # def __init__(self, username):
    #     self.username = username
    # mongoengine doesn't need init




@login.user_loader
def load_user(username):
    u = db.users.find_one({"username" : username})
    if not u:
        return None
    return User(username = u['username'])
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
############################
####### ROUTES ############
###########################

@app.route( '/' ) # home page
def index():
  return render_template( './chat_site_home.html' ) #using html file for this page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        user = db.users.find_one({'username': form.username.data})

        if user is None:
            user = {
                'username' : form.username.data,
                'last_seen' : datetime.datetime.now(),
                'messages_received' : None,
                'last_message_read_time' : datetime.datetime.now()
            }
            # user = User(username=form.username.data)
            community = db.users.insert_one(user) # for mongodb

        new_user = User(username=form.username.data) # for flask_login
        new_user.last_seen = datetime.datetime.now()
        new_user.last_message_read_time = datetime.datetime.now()
        new_user.save()
        login_user(new_user, force = True, fresh = True)

        #
        # # new_user = User(username=form.username.data)
        # # user2 = User(username = 'ex@wxample.com').save()
        # community = db.users.insert_one(new_user)
        # new_user.last_seen = datetime.datetime.now()
        # new_user.last_message_read_time = datetime.datetime.now()
        # community = db.users.update_one(new_user)

        # community = users.insert_one(user)

        return redirect(url_for('chat'))
    return render_template('cs_login.html', title='Sign In', form=form)

@app.route('/signup')
def signup():
    pass

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        # flash('Your message has been sent.')
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=('Send Message'),
                           form=form, recipient=recipient)


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def chat():

    form = MessageForm()
    if form.validate_on_submit():
        user = current_user
        msg = {
            'author' : user.username,
            'recipient' : form.recipient.data,
            'body' : form.body.data,
            'timestamp' : datetime.datetime.now()
        }
        chat = db.messages.insert_one(msg)
        community = db.users.insert_one(msg)

    new_message = Message(author=current_user.username,
                            recipient=form.recipient.data,
                            body=form.body.data,
                            timestamp=datetime.datetime.now())

    # add msg to user's messages_sent
    sending = User(username = current_user.username,
                    messages_sent=new_message).save()
    recieving = User(username=form.recipient.data,
                    messages_received=new_message).save()


     # {'username'=current_user.username, 'messages_sent'=new_message})

    flash(form.errors)

    page = request.args.get('page', 1, type=int)
    msgs = users['messages_received']
    # db.messages.messages_received
    # .order_by(
    #     Message.timestamp.desc()).paginate(
    #         page, current_app.config['POSTS_PER_PAGE'], False)

    # next_url = url_for('index', page=messages.next_num) \
    #     if messages.has_next else None
    # prev_url = url_for('login', page=messages.prev_num) \
    #     if messages.has_prev else None

    return render_template('messages.html', form=form, msgs=msgs)
                           # next_url=next_url, prev_url=prev_url)


if __name__ == '__main__':
  app.run(debug = True) #opens debug traceback
  # and with debug pin from console, gives a debugging console
