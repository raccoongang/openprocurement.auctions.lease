# -*- coding: utf-8 -*-
import unittest
import os
from copy import deepcopy
from datetime import datetime, timedelta

import mock
from schematics.exceptions import ConversionError, ValidationError, ModelValidationError

from openprocurement.auctions.lease.models import (
    ContractTerms
)


from openprocurement.api.utils import get_now

now = get_now()


class ContractTermsTest(unittest.TestCase):

    def test_ContractTerms_model(self):

        data = {"type": "lease", "leaseTerms": {"leaseDuration": "P10Y"}}

        contractterms = ContractTerms(data)

        contractterms.validate()

        contractterms.type = None
        self.assertNotEqual(contractterms.serialize(), data)
        with self.assertRaises(ModelValidationError) as ex:
            contractterms.validate()
        self.assertEqual(ex.exception.message,
                         {"type": ["This field is required."]})


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(ContractTermsTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
