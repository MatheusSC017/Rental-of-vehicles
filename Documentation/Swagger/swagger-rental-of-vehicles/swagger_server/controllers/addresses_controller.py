import connexion
import six

from swagger_server.models.address import Address  # noqa: E501
from swagger_server import util


def addresses_get():  # noqa: E501
    """Return a list of all addresses.

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def addresses_id_delete(id):  # noqa: E501
    """Delete an address

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def addresses_id_get(id):  # noqa: E501
    """Return an object containing address information

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def addresses_id_put(body, id):  # noqa: E501
    """Update an address and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def addresses_post(body):  # noqa: E501
    """Register a new address

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
