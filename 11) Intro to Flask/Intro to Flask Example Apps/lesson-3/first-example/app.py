# app.py

# request is another module to use on the thankyou page
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/thank_you')
def thank_you():
    first = request.args.get('first')
    last = request.args.get('last')
    # These go to where the get was used in a form and find which one had the label first or last, and grab the answer provided
    return render_template('thankyou.html', first=first, last=last)

@app.errorhandler(404)
def page_not_found(e):
    # The e is custom since it stands for error
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug)