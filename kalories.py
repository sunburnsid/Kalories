from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from clarifai.client import ClarifaiApi
import os
import tempfile
import base64
import hashlib


app = Flask(__name__)
app.config.from_pyfile('kalories.cfg')
db = SQLAlchemy(app)


class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    calcium = db.Column(db.Float)
    vitamins = db.Column(db.Float)
    healthy = db.Column(db.Boolean)
    calories=db.Column(db.Float)
    unit = db.Column(db.String(60))

    def __init__(self, name, protein, carbs, fat, fiber, calcium,
        vitamins, healthy, calories, unit):
        self.name     = name
        self.protein  = protein
        self.carbs    = carbs
        self.fat      = fat
        self.calcium  = calcium
        self.vitamins = vitamins
        self.healthy  = healthy
        self.calories = calories
        self.unit     = unit

class API(db.model):
    __tablename__ = 'api'
    date = db.Column(db.Integer)
    food = db.Column(db.Integer, ForeignKey(food.name))
    quantity = db.Column(db.Integer)
    url = db.Column(db.String)

    def __init__(self, date, food, quantity, url)


@app.route('/')
def show_all():
    return render_template('show_all.html',
        food=Food.query.order_by(Food.id.desc()).all()
    )


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            todo = Todo(request.form['title'], request.form['text'])
            db.session.add(todo)
            db.session.commit()
            flash(u'Todo item was successfully created')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/update', methods=['POST'])
def update_done():
    for todo in Todo.query.all():
        todo.done = ('done.%d' % todo.id) in request.form
    flash('Updated status')
    db.session.commit()
    return redirect(url_for('show_all'))


@app.route('/get_suggestions/<string:base_id>', methods=['GET'])
def getSuggestions(base_id):

    dest = "/static/" + abs(hash(base_id)) + ".png"

    with open(dest, "wb") as fh:
        fh.write(base_id.decode('base64'))

    #clarifai_api = ClarifaiApi() # assumes environment variables are set.
    #result = clarifai_api.tag_images(open(text, 'rb'))
    result = {u'status_code': u'OK', u'status_msg': u'All images in request have co$
    parsed = result['results'][0]['result']['tag']['classes']
    answer = []
    for val in parsed:
        if (db.session.query(food.name).filter_by(name=val).scalar() is not None):
            answer.append(val)
    return flask.jsonify(suggestions=answer, url=text)

@app.route('/confirmFood', methods=['POST'])
def confirmFood():
    values  = []
    content = request.get_json(silent=True)
    for food,amt in content['content']:
        values.add(session.query(food.protein, food.carbs, food.fat, food.fiber,
        food.calcium, food.vitamins, food.healthy, food.calories).filter_by(
        name = food).first())
    #multiply values by amt 
    return flask.jsonify(protein=protein,carbs=carbs, fat=fat,fiber=fiber,
    calcium=calcium, vitamins=vitamins, healthy=healthy, calories=calories)

@app.route('/getDay/<int:day>', methods = ['GET'])
def giveDay(day):
    dd  = day / 10000
    dd1 = day % 10000
    mm  = dd1 / 100
    yy  = dd1 % 100




if __name__ == '__main__':
app.run()
