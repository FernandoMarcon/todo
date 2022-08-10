from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os, datetime

app = Flask(__name__)

# client = MongoClient(username="root",password="example")
client = MongoClient('db',27017)
db = client.tododb

@app.route('/')
def todo():
    _items = db.tododb.find().sort('time')
    items = [item for item in _items]
    return render_template('todo.html', items=items)

@app.route('/new', methods=['POST'])
def new():

    item_doc = {
            'title': request.form['note-title'],
            'description': request.form['note-description'],
            'status': request.form['note-status'],
            'time': datetime.datetime.utcnow()
            }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))


@app.route('/get/<id>')
def get(id=None):
    if id:
        item = db.tododb.find_one({'_id':ObjectId(id)})
        print(item)
        return item['title']

@app.route('/rm/<id>')
def rm(id):
    # if id:
    item = db.tododb.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('todo'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run()
