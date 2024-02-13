import connexion
import six

from swagger_server.models.appointment_body import AppointmentBody  # noqa: E501
from swagger_server.models.appointment_id_body import AppointmentIdBody  # noqa: E501
from swagger_server.models.rent_id_body import RentIdBody  # noqa: E501
from swagger_server import util


def appointment_id_put(body, id):  # noqa: E501
    """Update an appointment and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = AppointmentIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def appointment_post(body):  # noqa: E501
    """Register a new appointment

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = AppointmentBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def rent_id_put(body, id):  # noqa: E501
    """Update a rent and return an object with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: object
    """
    if connexion.request.is_json:
        body = RentIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def rents_expired_appointments_get():  # noqa: E501
    """Return a list of all expired appointments

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def rents_expired_returns_get():  # noqa: E501
    """Return a list of all expired returns

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def rents_get():  # noqa: E501
    """Return a list of all rents

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def rents_id_appointment_to_rent_put(id):  # noqa: E501
    """Update the status of a rental from appointment to rented and return an object with the new values

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def rents_id_cancel_appointment_put(id):  # noqa: E501
    """Update the status of a rental from appointment to canceled and return an object with the new values

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def rents_id_get(id):  # noqa: E501
    """Return an object containing rent information

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'


def rents_id_vehicle_devolution_put(id):  # noqa: E501
    """Update the status of a rental from rented to returned and return an object with the new values

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: object
    """
    return 'do some magic!'
