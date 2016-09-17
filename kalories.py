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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    tempfile.gettempdir(), 'test.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)


class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column('food_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    calcium = db.Column(db.Float)
    vitamins = db.Column(db.Float)
    healthy = db.Column(db.Boolean)
    calories=db.Column(db.Float)
    unit = db.Column(db.String(60))

    def __init__(self, name, protein, carbs, fat, calcium,
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

class API(db.Model):
    __tablename__ = 'api'
    id = db.Column('api_id', db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    food = db.Column(db.Integer) #ForeignKey("food.name"))
    quantity = db.Column(db.Integer)
    url = db.Column(db.String)

    def __init__(self, date, food, quantity, url):
        self.date=date
        self.food=food
        self.quantity=quantity
        self.url=url

@app.route('/upload')
#import one time
def uploadcsv():
    with open('ABBREV.csv', 'rb') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            print row

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
    #result = clarifai_api.tag_images(open(dest, 'rb'))

    result = {u'status_code': u'OK', u'status_msg': u'All images in request have completed successfully. ', u'meta': {u'tag': {u'timestamp': 1474084104.627829, u'model': u'general-v1.3', u'config': None}}, u'results': [{u'docid': 42024272502422257284519421165328554557L, u'status_code': u'OK', u'status_msg': u'OK', u'local_id': u'', u'result': {u'tag': {u'classes': [u'carrot', u'root', u'food', u'no person', u'provitamin A', u'vegetable', u'nutrition', u'health', u'healthy', u'agriculture', u'diet', u'leaf', u'desktop', u'freshness', u'grow', u'close-up', u'juicy', u'bunch', u'ingredients', u'cooking'], u'concept_ids': [u'ai_DGvpjM5g', u'ai_3xJvggfW', u'ai_3PlgVmlN', u'ai_786Zr311', u'ai_grVmTvp7', u'ai_LpcgM7r5', u'ai_nl2sV1Hm', u'ai_mZ2tl6cW', u'ai_0mCQLwrm', u'ai_ZsprRgCn', u'ai_Cp0N9mF9', u'ai_wBCrHPDb', u'ai_Lq00FggW', u'ai_mZJ4nprg', u'ai_VRrpDkps', u'ai_4lvjn8qv', u'ai_gt6djlDq', u'ai_mXdcXbrT', u'ai_xzqBDlmV', u'ai_KXNqVd5F'], u'probs': [0.9975664615631104, 0.9955800175666809, 0.9922435283660889, 0.99013352394104, 0.9898305535316467, 0.9868329763412476, 0.9771294593811035, 0.9762943983078003, 0.9708182215690613, 0.9601856470108032, 0.956566572189331, 0.9558433294296265, 0.9373021125793457, 0.9226887226104736, 0.9224319458007812, 0.9132283329963684, 0.911675214767456, 0.9096507430076599, 0.9050804972648621, 0.8930140733718872]}}, u'docid_str': u'1f9d949a5c38fffe3e7e2f58c7ca5a3d'}]}
    parsed = result['results'][0]['result']['tag']['classes']
    answer = []
    result = {u'status_code': u'OK', u'status_msg': u'All images in request have completed successfully. ', u'meta': {u'tag': {u'timestamp': 1474084104.627829, u'model': u'general-v1.3', u'config': None}}, u'results': [{u'docid': 42024272502422257284519421165328554557L, u'status_code': u'OK', u'status_msg': u'OK', u'local_id': u'', u'result': {u'tag': {u'classes': [u'carrot', u'root', u'food', u'no person', u'provitamin A', u'vegetable', u'nutrition', u'health', u'healthy', u'agriculture', u'diet', u'leaf', u'desktop', u'freshness', u'grow', u'close-up', u'juicy', u'bunch', u'ingredients', u'cooking'], u'concept_ids': [u'ai_DGvpjM5g', u'ai_3xJvggfW', u'ai_3PlgVmlN', u'ai_786Zr311', u'ai_grVmTvp7', u'ai_LpcgM7r5', u'ai_nl2sV1Hm', u'ai_mZ2tl6cW', u'ai_0mCQLwrm', u'ai_ZsprRgCn', u'ai_Cp0N9mF9', u'ai_wBCrHPDb', u'ai_Lq00FggW', u'ai_mZJ4nprg', u'ai_VRrpDkps', u'ai_4lvjn8qv', u'ai_gt6djlDq', u'ai_mXdcXbrT', u'ai_xzqBDlmV', u'ai_KXNqVd5F'], u'probs': [0.9975664615631104, 0.9955800175666809, 0.9922435283660889, 0.99013352394104, 0.9898305535316467, 0.9868329763412476, 0.9771294593811035, 0.9762943983078003, 0.9708182215690613, 0.9601856470108032, 0.956566572189331, 0.9558433294296265, 0.9373021125793457, 0.9226887226104736, 0.9224319458007812, 0.9132283329963684, 0.911675214767456, 0.9096507430076599, 0.9050804972648621, 0.8930140733718872]}}, u'docid_str': u'1f9d949a5c38fffe3e7e2f58c7ca5a3d'}]}

    parsed= result['results'][0]['result']['tag']['classes']
    answer=[]
    for val in parsed:
        if (db.session.query(food.name).filter_by(name=val).scalar() is not None):
            answer.append(val)
    return flask.jsonify(suggestions=answer, url=text)

@app.route('/confirmFood', methods=['POST'])
def confirmFood():
    values  = []
    content = request.get_json(silent=True)
    #initialize values
    protein, carbs, fat, calcium, calories = (0 for i in range(5))
    vitamins=set()
    healthy=True
    content= request.get_json(silent=True)
    #iterate through list in json and accumulate nutrition values

    for food,amt in content['content']:
        values = session.query(food.protein, food.carbs, food.fat,
        food.calcium, food.vitamins, food.healthy, food.calories).filter_by(
        name = food).first()
        protein += values["protein"]*amt
        carbs += values["carbs"]*amt
        fat += values["fat"]*amt
        calcium += values["calcium"]
        calories += values["calories"]
        vitamins.add(values["vitamins"])
        healthy=values["healthy"]
    return flask.jsonify(protein=protein,carbs=carbs, fat=fat,fiber=fiber,
    calcium=calcium, vitamins=vitamins, healthy=healthy, calories=calories,
    url=content['url'])

@app.route('/getDay/<int:day>', methods = ['GET'])
def giveDay(day):


if __name__ == '__main__':
    app.run()
