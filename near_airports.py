from utils import find_value_in_dict
from datetime import datetime, timedelta
import requests
import pprint
import json

def geocode(human_address):
    """Returns the latitude and longitude of a human-readable address to 3 decimal plances.

    Args:
        human_address (string): Address such as '50 Onslow Gardens London United Kingdom'

    Returns:
        list: [lat, lng], each to 3dp.
    """
    
    goog_api_key = 'AIzaSyBBTBVgKMGeQRMyzyFT3ay-CvYF2ygTJ0I'
    goog_uri = 'https://maps.googleapis.com/maps/api/geocode/json'
    uri = goog_uri + '?address=' + human_address.replace(' ', '%20') + '&key=' + goog_api_key

    response = requests.get(uri)
    if response.status_code == 200:
        res = dict(response.json())
        loc = find_value_in_dict(res, 'location')
        lat = round(loc['lat'], 3)
        lng = round(loc['lng'], 3)
        return [lat, lng]
    else:
        print('Geocoder Failed')
        response.raise_for_status()

def find_closest_5_airports(lat, lng, token):
    """ 
    Returns a list of 5 closest airports to the latitude and longitude provided.
    The airports are in their 3 letter code (e.g. London Heathrow -> LHR)

    Args:
        lat (float): latitude
        lng (float): longitude

    Returns:
        list (5): 5 closest airport in their 3-letter code. 
    """
    lat, lng = round(lat, 3), round(lng, 3)
    uri = f"https://api.lufthansa.com/v1/references/airports/nearest/{lat},{lng}"
    headers = {
        'Authorization': f'Bearer {token} ',
        'Accept': 'application/json',
    }
    response = requests.get(uri, headers=headers)
    if response.status_code == 200:
        data_dict = dict(response.json())
        five_airport_array_with_too_much_data = data_dict['NearestAirportResource']['Airports']['Airport']
        airport_code_list = []
        for airport_obj in five_airport_array_with_too_much_data:
            airport_code_list.append(airport_obj['AirportCode'])
        return airport_code_list
    else:
        response.raise_for_status()

def get_token():
    """ 
    The API token given by LH has 1.5 days expiration. Before I make a call,
    I need to check if the token if it is still valid. If it is, proceed with 
    the call and if not I will generate a new token in another function.
    The current token is stored in a local json file.
    Returns if token is still valid.

    Returns:
        bool: True if token valid, False if not
    """
    now_timestamp = datetime.now().timestamp()
    with open('token.json','r') as file:
        token_obj = json.load(file)
    if token_obj["expires_in"] > now_timestamp:
        return token_obj["access_token"]

    url = "https://api.lufthansa.com/v1/oauth/token"
    data = {
        'client_id': 'ft7399pr9dqg2f9gunxcm2j2x',
        'client_secret': 'mj2XTBxTxh',
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        data_dict = dict(response.json())
        with open('token.json','w') as file:
            json.dump({
                "access_token": data_dict["access_token"],
                "token_type":"bearer",
                "expires_in": now_timestamp + data_dict["expires_in"],
            }, file)
        return data_dict["access_token"]
    else:
        response.raise_for_status()
