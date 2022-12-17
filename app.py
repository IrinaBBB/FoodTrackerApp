from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/view')
def view():
    return render_template('day.html')


@app.route('/add')
def add():
    return render_template('add_food.html')
