import connexion
import six

from swagger_server.models.branch import Branch  # noqa: E501
from swagger_server import util


def branches_get():  # noqa: E501
    """Return a list of all branches

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def branches_id_delete(id):  # noqa: E501
    """Delete a branch

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def branches_id_get(id):  # noqa: E501
    """Return an object containing branch information

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def branches_id_put(body, id):  # noqa: E501
    """Update a branch and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = Branch.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def branches_post(body):  # noqa: E501
    """Register a new Branch

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = Branch.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
