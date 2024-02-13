# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.appointment_body import AppointmentBody  # noqa: E501
from swagger_server.models.appointment_id_body import AppointmentIdBody  # noqa: E501
from swagger_server.models.rent_id_body import RentIdBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRentsController(BaseTestCase):
    """RentsController integration test stubs"""

    def test_appointment_id_put(self):
        """Test case for appointment_id_put

        Update an appointment and return an object with the new values
        """
        body = AppointmentIdBody()
        response = self.client.open(
            '//appointment/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_appointment_post(self):
        """Test case for appointment_post

        Register a new appointment
        """
        body = AppointmentBody()
        response = self.client.open(
            '//appointment',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rent_id_put(self):
        """Test case for rent_id_put

        Update a rent and return an object with the new values
        """
        body = RentIdBody()
        response = self.client.open(
            '//rent/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rents_expired_appointments_get(self):
        """Test case for rents_expired_appointments_get

        Return a list of all expired appointments
        """
        response = self.client.open(
            '//rents/expired_appointments',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rents_expired_returns_get(self):
        """Test case for rents_expired_returns_get

        Return a list of all expired returns
        """
        response = self.client.open(
            '//rents/expired_returns',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rents_get(self):
        """Test case for rents_get

        Return a list of all rents
        """
        response = self.client.open(
            '//rents',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rents_id_appointment_to_rent_put(self):
        """Test case for rents_id_appointment_to_rent_put

        Update the status of a rental from appointment to rented and return an object with the new values
        """
        response = self.client.open(
            '//rents/{id}/appointment_to_rent'.format(id='id_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rents_id_cancel_appointment_put(self):
        """Test case for rents_id_cancel_appointment_put

        Update the status of a rental from appointment to canceled and return an object with the new values
        """
        response = self.client.open(
            '//rents/{id}/cancel_appointment'.format(id='id_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rents_id_get(self):
        """Test case for rents_id_get

        Return an object containing rent information
        """
        response = self.client.open(
            '//rents/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rents_id_vehicle_devolution_put(self):
        """Test case for rents_id_vehicle_devolution_put

        Update the status of a rental from rented to returned and return an object with the new values
        """
        response = self.client.open(
            '//rents/{id}/vehicle_devolution'.format(id='id_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
