# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.customer import Customer  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCustomersController(BaseTestCase):
    """CustomersController integration test stubs"""

    def test_customers_cpf_delete(self):
        """Test case for customers_cpf_delete

        Delete a customer
        """
        response = self.client.open(
            '//customers/{cpf}'.format(cpf='cpf_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_cpf_get(self):
        """Test case for customers_cpf_get

        Return an object containing customer information
        """
        response = self.client.open(
            '//customers/{cpf}'.format(cpf='cpf_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_cpf_put(self):
        """Test case for customers_cpf_put

        Update a customer and return an object with the new values
        """
        body = Customer()
        response = self.client.open(
            '//customers/{cpf}'.format(cpf='cpf_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_get(self):
        """Test case for customers_get

        Return a list of all customers
        """
        response = self.client.open(
            '//customers',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_post(self):
        """Test case for customers_post

        Register a new customer
        """
        body = Customer()
        response = self.client.open(
            '//customers',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
