# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.insurance import Insurance  # noqa: E501
from swagger_server.test import BaseTestCase


class TestInsurancesController(BaseTestCase):
    """InsurancesController integration test stubs"""

    def test_insurances_get(self):
        """Test case for insurances_get

        Return a list of all vehicle insurances
        """
        response = self.client.open(
            '//insurances',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_insurances_id_delete(self):
        """Test case for insurances_id_delete

        Delete a vehicle insurance
        """
        response = self.client.open(
            '//insurances/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_insurances_id_get(self):
        """Test case for insurances_id_get

        Return an object containing vehicle insurance information
        """
        response = self.client.open(
            '//insurances/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_insurances_id_put(self):
        """Test case for insurances_id_put

        Update a vehicle insurance and return an object with the new values
        """
        body = Insurance()
        response = self.client.open(
            '//insurances/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_insurances_post(self):
        """Test case for insurances_post

        Register a new vehicle insurance
        """
        body = Insurance()
        response = self.client.open(
            '//insurances',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
