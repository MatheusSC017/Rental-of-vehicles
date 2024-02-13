import connexion
import six

from swagger_server.models.vehicle import Vehicle  # noqa: E501
from swagger_server import util


def branches_id_vehicles_get(id):  # noqa: E501
    """Return a list of all vehicles in a branch

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def vehicles_get():  # noqa: E501
    """Return a list of all vehicles

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def vehicles_post(body):  # noqa: E501
    """Register a new vehicle

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = Vehicle.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def vehicles_renavam_delete(renavam):  # noqa: E501
    """Delete a vehicle

     # noqa: E501

    :param renavam: 
    :type renavam: str

    :rtype: None
    """
    return 'do some magic!'


def vehicles_renavam_get(renavam):  # noqa: E501
    """Return an object containing vehicle information

     # noqa: E501

    :param renavam: 
    :type renavam: str

    :rtype: object
    """
    return 'do some magic!'


def vehicles_renavam_put(body, renavam):  # noqa: E501
    """Update a vehicle and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param renavam: 
    :type renavam: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = Vehicle.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
