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


class DummyContractTermsTest(unittest.TestCase):
    pass


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(DummyContractTermsTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
