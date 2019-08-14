import os, datetime, getpass
from chat_forms import LoginForm, MessageForm
from flask import Flask, render_template, url_for, redirect, request, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, \
AnonymousUserMixin, fresh_login_required
from flask_bootstrap import Bootstrap

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

client = pymongo.MongoClient("mongodb+srv://apouba:Codeyourdreams@cluster0-x2fzi.mongodb.net/test?retryWrites=true&w=majority")
# client = pymongo.MongoClient(mongodb+srv://apouba:<Codeyourdreams>@cluster0-x2fzi.mongodb.net/test?retryWrites=true&w=majority)
db = client.ChatInfo
messages = db.messages # collection
users = db.user # collection

Migrate(app,db)
login = LoginManager()
login.init_app(app)
bootstrap = Bootstrap(app)


##########################
### MODELS#################
#####################

user = {
    #'_id' : ObjectId(''),
    '_id' : db.users.count(),
    'username' : 'Guest',
    'last_seen' : datetime.datetime.now(),
    'messages_sent' : [ {}, ...],
        # {
        # 'None'
        # },
    'messages_received' : [{}, ...],
    'last_message_read_time' : datetime.datetime.now()
}

message = {
    #'_id' : ObjectId('message'),
    'sender_id' : "",
    'recipient_id' : "",
    'body' : "Empty message",
    'timestamp' : datetime.datetime.now()
}

@login.user_loader
def load_user(id):
    pass
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
        new_user = {
            'username' : form.username.data,
            'last_seen' : datetime.datetime.now(),
            'last_message_read_time' : datetime.datetime.now()
        }
        #user = User.query.filter_by(username=form.username.data).first()
        community = users.insert_one(new_user)
        # community.inserted_id


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
def chat():

    # db.users.replace_one({'username' : current_user },
    #                     {'last_message_read_time' : datetime.datetime.now()})
    form = MessageForm()
    message = 'form not working'
    if form.validate_on_submit():
        hey = "hey"
        new_message = {'sender_id' : 'guest21',
                                'recipient_id' : form.recipient.data,
                                'body' : form.body.data,
                                'timestamp' : '12'
        }
        chat = db.messages.insert_one(new_message)

    # print(hey)
    print(message)
    flash(form.errors)

    page = request.args.get('page', 1, type=int)
    messages = db.messages.messages_received
    # .order_by(
    #     Message.timestamp.desc()).paginate(
    #         page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('index', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('login', page=messages.prev_num) \
        if messages.has_prev else None

    return render_template('messages.html', form=form,
                           next_url=next_url, prev_url=prev_url)


if __name__ == '__main__':
  app.run(debug = True) #opens debug traceback
  # and with debug pin from console, gives a debugging console
