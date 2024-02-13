import connexion
import six

from swagger_server.models.insurance import Insurance  # noqa: E501
from swagger_server import util


def insurances_get():  # noqa: E501
    """Return a list of all vehicle insurances

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def insurances_id_delete(id):  # noqa: E501
    """Delete a vehicle insurance

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def insurances_id_get(id):  # noqa: E501
    """Return an object containing vehicle insurance information

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def insurances_id_put(body, id):  # noqa: E501
    """Update a vehicle insurance and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = Insurance.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def insurances_post(body):  # noqa: E501
    """Register a new vehicle insurance

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = Insurance.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
