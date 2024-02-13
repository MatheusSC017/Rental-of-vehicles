import connexion
import six

from swagger_server.models.customer import Customer  # noqa: E501
from swagger_server import util


def customers_cpf_delete(cpf):  # noqa: E501
    """Delete a customer

     # noqa: E501

    :param cpf: 
    :type cpf: str

    :rtype: None
    """
    return 'do some magic!'


def customers_cpf_get(cpf):  # noqa: E501
    """Return an object containing customer information

     # noqa: E501

    :param cpf: 
    :type cpf: str

    :rtype: object
    """
    return 'do some magic!'


def customers_cpf_put(body, cpf):  # noqa: E501
    """Update a customer and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param cpf: 
    :type cpf: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = Customer.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def customers_get():  # noqa: E501
    """Return a list of all customers

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def customers_post(body):  # noqa: E501
    """Register a new customer

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = Customer.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
