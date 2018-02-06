from server import server
from flask import jsonify, request
from models import RiskTypeDefinition


@server.route('/hello/', methods=['GET'])
def RiskHello():
    return 'Hello from risktypes'


@server.route('/risktypes', methods=['GET'])
def RiskTypesGet():
    risktypes = RiskTypeDefinition.query.all()
    return jsonify({'data': [x.serialize for x in risktypes]})


@server.route('/risktypes/<risktype>', methods=['GET'])
def RiskTypeGet(risktype):
    data = {}
    return jsonify({'data': data})

