# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.address import Address  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAddressesController(BaseTestCase):
    """AddressesController integration test stubs"""

    def test_addresses_get(self):
        """Test case for addresses_get

        Return a list of all addresses.
        """
        response = self.client.open(
            '//addresses',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_addresses_id_delete(self):
        """Test case for addresses_id_delete

        Delete an address
        """
        response = self.client.open(
            '//addresses/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_addresses_id_get(self):
        """Test case for addresses_id_get

        Return an object containing address information
        """
        response = self.client.open(
            '//addresses/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_addresses_id_put(self):
        """Test case for addresses_id_put

        Update an address and return an object with the new values
        """
        body = Address()
        response = self.client.open(
            '//addresses/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_addresses_post(self):
        """Test case for addresses_post

        Register a new address
        """
        body = Address()
        response = self.client.open(
            '//addresses',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
