# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server.test import BaseTestCase


class TestClassificationsController(BaseTestCase):
    """ClassificationsController integration test stubs"""

    def test_classifications_get(self):
        """Test case for classifications_get

        Return a list of all vehicle classifications
        """
        response = self.client.open(
            '//classifications',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_classifications_id_delete(self):
        """Test case for classifications_id_delete

        Delete a vehicle classification
        """
        response = self.client.open(
            '//classifications/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_classifications_id_get(self):
        """Test case for classifications_id_get

        Return an object containing vehicle classification information
        """
        response = self.client.open(
            '//classifications/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_classifications_id_put(self):
        """Test case for classifications_id_put

        Update a vehicle classification and return an object with the new values
        """
        body = Classification()
        response = self.client.open(
            '//classifications/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_classifications_post(self):
        """Test case for classifications_post

        Register a new vehicle classification
        """
        body = Classification()
        response = self.client.open(
            '//classifications',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
