# app.py
from flask import Flask, render_template

app = Flask(__name__)

# Keep a global set of students for our web app to keep track of
students = ['Janet', 'Michael', 'Isabelle', 'Trish', 'Gabe']

@app.route('/')
def index():
    school_name = "Middleton High School"
    return render_template('index.html', school_name=school_name, students=students)

@app.route('/student/<name>')
def student(name):
    return render_template('student.html', student=name)

if __name__ == '__main__':
    app.run(debug=True, port=9874)