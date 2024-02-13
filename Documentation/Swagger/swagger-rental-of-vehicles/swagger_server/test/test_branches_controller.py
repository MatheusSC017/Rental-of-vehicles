# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.branch import Branch  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBranchesController(BaseTestCase):
    """BranchesController integration test stubs"""

    def test_branches_get(self):
        """Test case for branches_get

        Return a list of all branches
        """
        response = self.client.open(
            '//branches',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_branches_id_delete(self):
        """Test case for branches_id_delete

        Delete a branch
        """
        response = self.client.open(
            '//branches/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_branches_id_get(self):
        """Test case for branches_id_get

        Return an object containing branch information
        """
        response = self.client.open(
            '//branches/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_branches_id_put(self):
        """Test case for branches_id_put

        Update a branch and return an object with the new values
        """
        body = Branch()
        response = self.client.open(
            '//branches/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_branches_post(self):
        """Test case for branches_post

        Register a new Branch
        """
        body = Branch()
        response = self.client.open(
            '//branches',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
