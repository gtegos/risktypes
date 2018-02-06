import inspect, os
from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS
from models import db

from datetime import datetime


class AppJSONEncoder(JSONEncoder):
    ''' Specialized JSONEncoder to handle Pyhton datetime objects
    '''
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


server = Flask(__name__)
server.config['JSON_AS_ASCII'] = False
server.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nbt9832@localhost:5432/britecore'
server.config['APP_DB_NAME'] = 'postgresql'
server.config['APP_VERSION'] = '1.0.0.0'

server.json_encoder = AppJSONEncoder

CORS(server)

rootPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

db.init_app(server)

from rest import *


'''
# create the database
with server.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    db.create_all()
'''
