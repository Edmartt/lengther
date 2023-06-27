from flask import make_response
from . import locations_routes


@locations_routes.after_app_request
def after_request(data):
    '''
    Every response from this app is returned in json
    '''
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    return response
