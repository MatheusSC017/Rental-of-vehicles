# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Branch(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, opening_hours_start: str=None, opening_hours_end: str=None, address: str=None):  # noqa: E501
        """Branch - a model defined in Swagger

        :param name: The name of this Branch.  # noqa: E501
        :type name: str
        :param opening_hours_start: The opening_hours_start of this Branch.  # noqa: E501
        :type opening_hours_start: str
        :param opening_hours_end: The opening_hours_end of this Branch.  # noqa: E501
        :type opening_hours_end: str
        :param address: The address of this Branch.  # noqa: E501
        :type address: str
        """
        self.swagger_types = {
            'name': str,
            'opening_hours_start': str,
            'opening_hours_end': str,
            'address': str
        }

        self.attribute_map = {
            'name': 'name',
            'opening_hours_start': 'opening_hours_start',
            'opening_hours_end': 'opening_hours_end',
            'address': 'address'
        }
        self._name = name
        self._opening_hours_start = opening_hours_start
        self._opening_hours_end = opening_hours_end
        self._address = address

    @classmethod
    def from_dict(cls, dikt) -> 'Branch':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Branch of this Branch.  # noqa: E501
        :rtype: Branch
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Branch.


        :return: The name of this Branch.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Branch.


        :param name: The name of this Branch.
        :type name: str
        """

        self._name = name

    @property
    def opening_hours_start(self) -> str:
        """Gets the opening_hours_start of this Branch.


        :return: The opening_hours_start of this Branch.
        :rtype: str
        """
        return self._opening_hours_start

    @opening_hours_start.setter
    def opening_hours_start(self, opening_hours_start: str):
        """Sets the opening_hours_start of this Branch.


        :param opening_hours_start: The opening_hours_start of this Branch.
        :type opening_hours_start: str
        """

        self._opening_hours_start = opening_hours_start

    @property
    def opening_hours_end(self) -> str:
        """Gets the opening_hours_end of this Branch.


        :return: The opening_hours_end of this Branch.
        :rtype: str
        """
        return self._opening_hours_end

    @opening_hours_end.setter
    def opening_hours_end(self, opening_hours_end: str):
        """Sets the opening_hours_end of this Branch.


        :param opening_hours_end: The opening_hours_end of this Branch.
        :type opening_hours_end: str
        """

        self._opening_hours_end = opening_hours_end

    @property
    def address(self) -> str:
        """Gets the address of this Branch.


        :return: The address of this Branch.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address: str):
        """Sets the address of this Branch.


        :param address: The address of this Branch.
        :type address: str
        """

        self._address = address