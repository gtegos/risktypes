from server import server
from flask import jsonify, request


@server.route('/risktypes/<risktype>', methods=['GET'])
def RiskTypeGet(risktype):
    data = {}
    return jsonify({'data': data})

