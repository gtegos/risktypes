from server import server
from flask import jsonify, request
from models import RiskTypeDefinition


@server.route('/risktypes', methods=['GET'])
def RiskTypesGet():
    ''' Return a list of defined risk types
        together with their field definitions
    '''
    risktypes = RiskTypeDefinition.query.order_by(RiskTypeDefinition.name).all()
    return jsonify({'data': [x.serialize for x in risktypes]})


@server.route('/risktypes/<risktype>', methods=['GET'])
def RiskTypeGet(risktype):
    ''' Return a specific risk type definition
        together with it's field definitions
    '''
    risktype = RiskTypeDefinition.query.filter_by(name=risktype).first()
    return jsonify({'data': risktype.serialize})

