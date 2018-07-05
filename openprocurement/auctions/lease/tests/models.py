# -*- coding: utf-8 -*-
import unittest
import mock
import munch

from schematics.exceptions import ConversionError, ValidationError, ModelValidationError

from openprocurement.auctions.lease.models import (
   ContractTerms
)

from openprocurement.api.utils import get_now


now = get_now()


class ContractTermsTest(unittest.TestCase):

    @mock.patch('openprocurement.auctions.lease.models.get_auction')
    def test_ContractTerms_model(self, mock_get_auction):

        data = {"type": "lease", "leaseTerms": {"leaseDuration": "P10Y",
        "taxHolidays": [
            {
                "taxHolidaysDuration": "P5M",
                "conditions": "conditions description",
                "value": {
                    "amount": 100.0,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ],
         "escalationClauses": [
            {
                "escalationPeriodicity": "P5M",
                "escalationStepPercentage": 0.1,
                "conditions": "conditions description"
            }
        ]
        }}

        contractterms = ContractTerms(data)

        value_currency = munch.Munch({"currency": "UAH"})
        mock_get_auction.return_value = munch.Munch({'value':value_currency})

        contractterms.validate()

        contractterms.type = None
        self.assertNotEqual(contractterms.serialize(), data)
        with self.assertRaises(ModelValidationError) as ex:
            contractterms.validate()
        self.assertEqual(ex.exception.message,
                         {"type": ["This field is required."]})

        contractterms = ContractTerms(data)

        contractterms.validate()

        contractterms.leaseTerms['taxHolidays'][0]['taxHolidaysDuration'] = None
        contractterms.leaseTerms['taxHolidays'][0]['conditions'] = None
        contractterms.leaseTerms['taxHolidays'][0]['value'] = None
        self.assertNotEqual(contractterms.serialize(), data)
        with self.assertRaises(ModelValidationError) as ex:
            contractterms.validate()
        self.assertEqual(ex.exception.message,
                         {'leaseTerms': {'taxHolidays': [{'taxHolidaysDuration': [u'This field is required.'], 'conditions': [u'This field is required.'], 'value': [u'This field is required.']}]}})

        contractterms = ContractTerms(data)

        contractterms.validate()

        contractterms.leaseTerms['escalationClauses'][0]['escalationPeriodicity'] = None
        contractterms.leaseTerms['escalationClauses'][0]['conditions'] = None
        self.assertNotEqual(contractterms.serialize(), data)
        with self.assertRaises(ModelValidationError) as ex:
            contractterms.validate()
        self.assertEqual(ex.exception.message,
                         {'leaseTerms': {'escalationClauses': [{'conditions': [u'This field is required.'], 'escalationPeriodicity': [u'This field is required.']}]}})

        contractterms = ContractTerms(data)

        contractterms.validate()

        contractterms.leaseTerms['taxHolidays'][0]['value']['currency'] = 'USD'
        self.assertNotEqual(contractterms.serialize(), data)
        with self.assertRaises(ModelValidationError) as ex:
            contractterms.validate()
        self.assertEqual(ex.exception.message,
                         {'leaseTerms': {'taxHolidays': [{'value': [u'currency of taxHolidays value should be identical to currency of value of auction']}]}})

        contractterms = ContractTerms(data)

        contractterms.leaseTerms['taxHolidays'][0]['value']['currency'] = 'UAH'

        contractterms.validate()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(ContractTermsTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
