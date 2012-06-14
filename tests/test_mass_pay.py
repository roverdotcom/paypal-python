# coding=utf-8

import re
import unittest
from paypal_api import PayPalAPIResponseError
from . import interface_factory
from . import api_details

interface = interface_factory.get_interface_obj()

class TestMassPay(unittest.TestCase):

    def setUp(self):
        self.mass_pay = {
            'receivertype': 'EmailAddress',
            'l_email0': api_details.EMAIL_PERSONAL,
            'l_amt0': '19.71',
            'currencycode': 'USD',
        }

    # def test_mass_pay(self):
    #     response = interface.do_mass_pay(**self.mass_pay)
    #     self.assertTrue(response.success)
    #     self.assertIsInstance(response.correlationid, basestring)
    #     self.assertIsInstance(response.timestamp, basestring)
    #     self.assertIsInstance(response.build, basestring)
    #     self.assertIsInstance(response.version, basestring)

    def test_exception_handling(self):
        """
        Make sure response exception handling is working as intended
        (by omitting required l_email0 parameter.)
        """
        new_mass_pay = self.mass_pay
        del new_mass_pay['l_email0']
        self.assertNotIn('l_email0', new_mass_pay)

        # Make sure this raises an exception.
        raised = False
        try:
            interface.do_mass_pay(**new_mass_pay)
        except PayPalAPIResponseError as error:
            raised = True
            self.assertIsInstance(error, PayPalAPIResponseError)
            self.assertIsInstance(error.response.correlationid, basestring)
            long_msg = error.response.l_longmessage0
            self.assertTrue(re.search('email is missing', long_msg))
        self.assertTrue(raised)
