import os
from flask import Flask, jsonify
from flask.ext.cors import *

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
@cross_origin()
def get_tasks():
    return jsonify( { 'tasks': tasks } )

@app.route('/')
def hello():
    return 'Hello Heroku!'
