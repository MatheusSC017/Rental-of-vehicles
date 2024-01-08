import requests
import math
import os


def singleton(target_class):
    instances = dict()

    def get_class(*args, **kwargs):
        if target_class not in instances:
            instances[target_class] = target_class(*args, **kwargs)
        return instances[target_class]

    return get_class


def geocoding(address, region='br'):
    """
    Get the coordinates (latitude and longitude) for a given address using the Google Maps Geocoding API.

    :param address: Dictionary containing address components (street, number, district, city, state, country).
    :param region: The region/country code for the geocoding request. Default is 'br' (Brazil).
    :return: List containing latitude and longitude.
    """
    BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    fields_order = ['street', 'number', 'complement', 'district', 'city', 'state', 'cep', 'country']
    address_string = ', '.join([str(address.get(field)) for field in fields_order if address.get(field)])

    params = {
        'address': address_string,
        'sensor': False,
        'region': region,
        'key': os.environ.get('GOOGLE_MAPS_SECRET_KEY')
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        result = response.json()
        if 'results' not in result or not result['results']:
            raise ValueError("Invalid Address, no coordinates were found for the address provided")

        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']

        return [lat, lng]
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error in geocoding request: {e}")


def haversine_distance(start_coordinate, end_coordinate):
    EARTH_RADIUS = 3958.8
    radius_start_lat = start_coordinate[0] * (math.pi/180)
    radius_end_lat = end_coordinate[0] * (math.pi/180)
    difference_lat = radius_start_lat - radius_end_lat
    difference_lng = (start_coordinate[1] - end_coordinate[1]) * (math.pi/180)

    distance = 2 * EARTH_RADIUS * math.asin(math.sqrt(
        math.pow(math.sin(difference_lat / 2), 2) +
        math.cos(radius_start_lat) *
        math.cos(radius_end_lat) *
        math.pow(math.sin(difference_lng / 2), 2))
    )

    return distance * 1609.344
