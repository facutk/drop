import os, datetime, calendar, json, requests
from flask import Flask, jsonify, request, abort, make_response, url_for
from werkzeug.contrib.cache import SimpleCache
from werkzeug.utils import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] #'sqlite:///app.db'
db = SQLAlchemy(app)

cache = SimpleCache()
cache.set('greeting', 0)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    count = db.Column( db.Integer )
    
    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False,
        'timestamp': datetime.datetime.utcnow()
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False,
        'timestamp': datetime.datetime.utcnow()
    }
]

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def make_public_task(task):
    new_task = {}
    for field in task:
        new_task[field] = task[field]
        if field == 'timestamp':
            new_task['timestamp'] = calendar.timegm( task['timestamp'].utctimetuple() )
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
    return new_task

@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get( 'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': map(make_public_task, tasks) } )
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': make_public_task(task[0]) } )
 
@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False,
        'timestamp': datetime.datetime.utcnow()
    }
    tasks.append(task)
    return jsonify( { 'task': make_public_task(task) } ), 201
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    task[0]['timestamp'] = datetime.datetime.utcnow()
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )

@app.route('/todo/api/v1.0/tasks/image', methods=['POST'])
def image():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save( filename )
            url = os.environ['DROP_IMG_STORAGE']
            files = {'file': ( filename, open(filename, 'rb')) }
            data = {'secret': os.environ['DROP_IMG_SECRET'] }
            r = requests.post(url, data=data, files=files)
            return jsonify( { 'result': True } )
    jsonify( { 'result': 'Error' } )
    
def image():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save( filename )
            url = os.environ['DROP_IMG_STORAGE']
            files = {'file': ( filename, open(filename, 'rb')) }
            data = {'secret': os.environ['DROP_IMG_SECRET'] }
            r = requests.post(url, data=data, files=files)
            return jsonify( { 'result': True } )
    jsonify( { 'result': 'Error' } )
    
@app.route('/greeting')
def greeting():
    greeting = cache.get('greeting')
    cache.set('greeting', greeting + 1)
    return jsonify( {'id': greeting, 'content': 'Hello, World!'} )

@app.route('/counters', methods=['GET'])
def get_counters():
    return jsonify( { 'counters':[ c.as_dict for c in Counter.query.all() ] } )
    
@app.route('/')
def hello():
    return 'Hello Heroku!'
