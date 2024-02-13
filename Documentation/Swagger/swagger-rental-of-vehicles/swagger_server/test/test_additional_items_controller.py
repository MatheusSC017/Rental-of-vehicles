# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.additional_item import AdditionalItem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAdditionalItemsController(BaseTestCase):
    """AdditionalItemsController integration test stubs"""

    def test_additional_items_get(self):
        """Test case for additional_items_get

        Return a list of all additional items for vehicles.
        """
        response = self.client.open(
            '//additional_items',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_additional_items_id_delete(self):
        """Test case for additional_items_id_delete

        Delete an additional item
        """
        response = self.client.open(
            '//additional_items/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_additional_items_id_get(self):
        """Test case for additional_items_id_get

        Return an object containing additional item information
        """
        response = self.client.open(
            '//additional_items/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_additional_items_id_put(self):
        """Test case for additional_items_id_put

        Update an additional item and return an object with the new values
        """
        body = AdditionalItem()
        response = self.client.open(
            '//additional_items/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_additional_items_post(self):
        """Test case for additional_items_post

        Register a new additional item for vehicles
        """
        body = AdditionalItem()
        response = self.client.open(
            '//additional_items',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_branches_id_additional_items_get(self):
        """Test case for branches_id_additional_items_get

        Return a list of all additional items for vehicles in a branch.
        """
        response = self.client.open(
            '//branches/{id}/additional_items'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
