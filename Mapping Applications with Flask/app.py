from flask import Flask, render_template, render_template, url_for, flash
# from wtforms import

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('map.html')



if __name__ == '__main__':
    app.run(debug=True)
