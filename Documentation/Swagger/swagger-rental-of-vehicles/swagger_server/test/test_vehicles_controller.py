# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.vehicle import Vehicle  # noqa: E501
from swagger_server.test import BaseTestCase


class TestVehiclesController(BaseTestCase):
    """VehiclesController integration test stubs"""

    def test_branches_id_vehicles_get(self):
        """Test case for branches_id_vehicles_get

        Return a list of all vehicles in a branch
        """
        response = self.client.open(
            '//branches/{id}/vehicles'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_vehicles_get(self):
        """Test case for vehicles_get

        Return a list of all vehicles
        """
        response = self.client.open(
            '//vehicles',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_vehicles_post(self):
        """Test case for vehicles_post

        Register a new vehicle
        """
        body = Vehicle()
        response = self.client.open(
            '//vehicles',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_vehicles_renavam_delete(self):
        """Test case for vehicles_renavam_delete

        Delete a vehicle
        """
        response = self.client.open(
            '//vehicles/{renavam}'.format(renavam='renavam_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_vehicles_renavam_get(self):
        """Test case for vehicles_renavam_get

        Return an object containing vehicle information
        """
        response = self.client.open(
            '//vehicles/{renavam}'.format(renavam='renavam_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_vehicles_renavam_put(self):
        """Test case for vehicles_renavam_put

        Update a vehicle and return an object with the new values
        """
        body = Vehicle()
        response = self.client.open(
            '//vehicles/{renavam}'.format(renavam='renavam_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
