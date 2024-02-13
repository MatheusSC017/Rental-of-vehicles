# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_customers_users_get(self):
        """Test case for customers_users_get

        Return a list of all users
        """
        response = self.client.open(
            '//customers/users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_users_id_delete(self):
        """Test case for customers_users_id_delete

        Delete an user
        """
        response = self.client.open(
            '//customers/users/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_users_id_get(self):
        """Test case for customers_users_id_get

        Return an object containing user information
        """
        response = self.client.open(
            '//customers/users/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_users_id_put(self):
        """Test case for customers_users_id_put

        Update an user and return an object with the new values
        """
        body = User()
        response = self.client.open(
            '//customers/users/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_customers_users_post(self):
        """Test case for customers_users_post

        Register a new user
        """
        body = User()
        response = self.client.open(
            '//customers/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
