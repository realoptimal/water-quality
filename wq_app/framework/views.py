from flask_restful import Resource

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
    def get(self, id=None):
        ''' Return Water Sample Info '''
        return 'This is a GET response'

    def post(self):
        ''' Create a new water sample '''
        return 'This is a POST response'

    def delete(self, id):
        ''' Delete the water sample with given id '''
        return 'This is a DELETE response'
