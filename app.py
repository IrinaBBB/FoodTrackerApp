from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


def connect_db():
    sql = sqlite3.connect('C:\\Users\\Bruker\\Desktop\\python\\FoodTrackerApp\\db\\food_log.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    if request.method == 'POST':
        date = request.form['date']
        dt = datetime.strptime(date, '%Y-%m-%d')
        database_date = datetime.strftime(dt, '%Y%m%d')
        db.execute('insert into log_date(entry_date) values(?)', [database_date])
        db.commit()

    cursor = db.execute('select entry_date from log_date order by entry_date desc ')
    results = cursor.fetchall()
    pretty_results = []
    for result in results:
        single_date = {}
        date_object = datetime.strptime(str(result['entry_date']), '%Y%m%d')
        single_date['entry_date'] = datetime.strftime(date_object, '%B %d, %Y')
        pretty_results.append(single_date)

    return render_template('home.html', results=pretty_results)


@app.route('/view')
def view():
    return render_template('day.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    db = get_db()
    if request.method == 'POST':
        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = protein * 4 + carbohydrates * 4 + fat * 9

        db.execute('insert into food(name, protein, carbohydrates, fat, calories) values(?, ?, ?, ?, ? )',
                   [name, protein, carbohydrates, fat, calories])
        db.commit()
    cursor = db.execute('select name, protein, carbohydrates, fat, calories from food')
    results = cursor.fetchall()
    return render_template('add_food.html', results=results)
