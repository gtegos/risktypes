import inspect, os
from flask import Flask
from flask.json import JSONEncoder
from flask_compress import Compress
from flask_cors import CORS

from datetime import datetime


class ClustersJSONEncoder(JSONEncoder):

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

server.config['APP_DB_NAME'] = 'postgresql'
server.config['APP_VERSION'] = '1.0.0.0'

server.json_encoder = ClustersJSONEncoder

Compress(server)
CORS(server)

rootPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

from controllers.risktypes import *
