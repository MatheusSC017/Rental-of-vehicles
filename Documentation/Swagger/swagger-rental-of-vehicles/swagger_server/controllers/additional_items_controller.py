import connexion
import six

from swagger_server.models.additional_item import AdditionalItem  # noqa: E501
from swagger_server import util


def additional_items_get():  # noqa: E501
    """Return a list of all additional items for vehicles.

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def additional_items_id_delete(id):  # noqa: E501
    """Delete an additional item

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def additional_items_id_get(id):  # noqa: E501
    """Return an object containing additional item information

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def additional_items_id_put(body, id):  # noqa: E501
    """Update an additional item and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = AdditionalItem.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def additional_items_post(body):  # noqa: E501
    """Register a new additional item for vehicles

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = AdditionalItem.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def branches_id_additional_items_get(id):  # noqa: E501
    """Return a list of all additional items for vehicles in a branch.

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'
