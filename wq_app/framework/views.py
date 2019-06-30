from flask import jsonify
from flask_restful import Resource, abort, reqparse

from wq_app import db
from wq_app.framework.models import *

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('description', type=str)
parser.add_argument('default_strength', type=float)
parser.add_argument('site', type=str)
parser.add_argument('contaminant_concentrations', type=list, location='json')
parser.add_argument('contaminant_strengths', type=list, location='json')

class SampleApi(Resource):
    def get(self, sample_id=None):
        ''' Return sample with given sample_id or all samples
            if none is specified.
        '''
        if not sample_id:
            samples = Sample.query.all()
        else:
            samples = [Sample.query.get(sample_id)]
        if not any(samples):
            abort(404, message='No sample(s) found given request.')
        res = {}
        for sample in samples:
            _cc_list_of_dicts = [{'contaminant_id': c.contaminant_id, 'concentration': c.concentration} for c in sample.contaminant_concentrations]
            res[sample.id] = {
                'site': sample.site,
                'contaminant_concentrations': _cc_list_of_dicts
            }
        return jsonify(res)

    def post(self):
        ''' Create sample and return it linked to sample_id 
            Will also create any sample linked contaminant concentration
            records.
        '''
        args = parser.parse_args()
        site = args['site']
        contaminant_concentrations = args['contaminant_concentrations']
        sample = Sample(site=site)
        db.session.add(sample)
        for cc in contaminant_concentrations:
            sample_cc = SampleContaminantConcentration(**cc)
            sample.contaminant_concentrations.append(sample_cc)
            db.session.add(sample_cc)
        db.session.commit()
        res = {}
        _cc_list_of_dicts = [{'contaminant_id': c.contaminant_id, 'concentration': c.concentration} for c in sample.contaminant_concentrations]
        res[sample.id] = {
            'site': sample.site,
            'contaminant_concentrations': _cc_list_of_dicts
        }
        return jsonify(res)

    def delete(self, sample_id):
        ''' Delete sample with given sample_id '''
        sample = Sample.query.get(sample_id)
        if not sample:
            abort(404, message='No sample found with that id.')
        db.session.delete(sample)
        db.session.commit()
        return jsonify({'response': 'Success'})


class FactorApi(Resource):
    def get(self, factor_id=None):
        ''' Return factor with given factor_id or all factors
            if none is specified.
        '''
        if not factor_id:
            factors = Factor.query.all()
        else:
            factors = [Factor.query.get(factor_id)]
        if not any(factors):
            abort(404, message='No factor(s) found given request.')
        res = {}
        for factor in factors:
            _cs_list_of_dicts = [{'contaminant_id': c.contaminant_id, 'strength': c.strength} for c in factor.contaminant_strengths]
            res[factor.id] = {
                'description': factor.description,
                'contaminant_strengths': _cs_list_of_dicts
            }
        return jsonify(res)

    def post(self):
        ''' Create factor and return it linked to factor_id 
            Will also create any factor linked contaminant strength
            records.
        '''
        args = parser.parse_args()
        description = args['description']
        contaminant_strengths = args['contaminant_strengths']
        factor = Factor(description=description)
        db.session.add(factor)
        for cs in contaminant_strengths:
            factor_cs = FactorContaminantStrength(**cs)
            factor.contaminant_strengths.append(factor_cs)
            db.session.add(factor_cs)
        db.session.commit()
        res = {}
        _cs_list_of_dicts = [{'contaminant_id': c.contaminant_id, 'strength': c.strength} for c in factor.contaminant_strengths]
        res[factor.id] = {
            'description': factor.description,
            'contaminant_strengths': _cs_list_of_dicts
        }
        return jsonify(res)

    def delete(self, factor_id):
        ''' Delete sample with given sample_id '''
        factor = Factor.query.get(factor_id)
        if not factor:
            abort(404, message='No factor found with that id.')
        db.session.delete(factor)
        db.session.commit()
        return jsonify({'response': 'Success'})


class ContaminantApi(Resource):
    def get(self, contaminant_id=None):
        ''' Return contaminant with given contaminant_id or all contaminants
            if none is specified.
        '''
        if not contaminant_id:
            contaminants = Contaminant.query.all()
        else:
            contaminants = [Contaminant.query.get(contaminant_id)]
        if not any(contaminants):
            abort(404, message='No contaminant(s) found given request.')
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
            abort(404, message='No contaminant found with that id.')
        db.session.delete(contaminant)
        db.session.commit()
        return jsonify({'response': 'Success'})
