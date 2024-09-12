from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from utils import find_value_in_dict
from api_fetcher import geocode, find_closest_5_airports, get_token
import requests
import pprint

app = Flask(__name__)
api = Api(app)

class ClosestAirportList(Resource):
    """ 
    This route returns an array of the 5 closest airports to
    a human-readable address.
    Each airport is in its 3 letters name identifier.
    For example, Manchester -> MAN, Heathrow -> LHR.
    """
    def get(self, human_address):
        human_address = human_address.replace('-', ' ')
        # Three API Calls
        lat, lng = geocode(human_address) # 
        token = get_token()
        five_closest_airports = find_closest_5_airports(lat, lng, token)
        return five_closest_airports

api.add_resource(ClosestAirportList, '/<string:human_address>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
