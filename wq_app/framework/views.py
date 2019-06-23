from flask import jsonify
from flask_restful import Resource, abort, reqparse

from wq_app import db
from wq_app.framework.models import *

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)
parser.add_argument('default_strength', type=float)

class SampleApi(Resource):
    def get(self, id=None):
        ''' Return Water Sample Info '''
        return 'This is a GET response'

    def post(self):
        ''' Create a new water sample '''
        return 'This is a POST response'

    def delete(self, id):
        ''' Delete the water sample with given id '''
        return 'This is a DELETE response'


class FactorApi(Resource):
    def get(self, id=None):
        ''' Return Water Sample Info '''
        return 'This is a GET response'

    def post(self):
        ''' Create a new water sample '''
        return 'This is a POST response'

    def delete(self, id):
        ''' Delete the water sample with given id '''
        return 'This is a DELETE response'


class ContaminantApi(Resource):
    def get(self, contaminant_id=None):
        ''' Return contaminant with given contaminant_id; or all contaminants
            if none is provided.
        '''
        if not contaminant_id:
            contaminants = Contaminant.query.all()
        else:
            contaminants = [Contaminant.query.get(contaminant_id)]
        if not any(contaminants):
            abort(404, message='No contaminants found given request.')
        res = {}
        for contaminant in contaminants:
            res[contaminant.id] = {
                'name': contaminant.name,
                'description': contaminant.description,
                'default_strength': contaminant.default_strength
            }
        return jsonify(res)

    def post(self):
        ''' Create contaminant and return it linked to contamaninant_id '''
        args = parser.parse_args()
        name = args['name']
        description = args['description']
        default_strength = args['default_strength']
        contaminant = Contaminant(name=name, description=description, default_strength=default_strength)
        db.session.add(contaminant)
        db.session.commit()
        res = {}
        res[contaminant.id] = {
            'name': contaminant.name,
            'description': contaminant.description,
            'default_strength': contaminant.default_strength
        }
        return jsonify(res)

    def delete(self, contaminant_id):
        ''' Delete contaminant with given contaminant_id '''
        contaminant = Contaminant.query.get(contaminant_id)
        if not contaminant:
            abort(404, message='No contaminant found with that ID.')
        db.session.delete(contaminant)
        db.session.commit()
        return jsonify({'response': 'Success'})
