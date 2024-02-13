import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def customers_users_get():  # noqa: E501
    """Return a list of all users

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def customers_users_id_delete(id):  # noqa: E501
    """Delete an user

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def customers_users_id_get(id):  # noqa: E501
    """Return an object containing user information

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def customers_users_id_put(body, id):  # noqa: E501
    """Update an user and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def customers_users_post(body):  # noqa: E501
    """Register a new user

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
