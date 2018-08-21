# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from openprocurement.auctions.core.constants import TZ

# document types
DOCUMENT_TYPE_OFFLINE = ['x_dgfAssetFamiliarization']
DOCUMENT_TYPE_URL_ONLY = ['virtualDataRoom']

# requiremnt periods
MINIMAL_EXPOSITION_PERIOD = timedelta(days=6)
MINIMAL_PERIOD_FROM_RECTIFICATION_END = timedelta(days=5)

# time constants
DGF_ID_REQUIRED_FROM = datetime(2017, 1, 1, tzinfo=TZ)
CLASSIFICATION_PRECISELY_FROM = datetime(2017, 7, 19, tzinfo=TZ)
MINIMAL_EXPOSITION_REQUIRED_FROM = datetime(2017, 11, 17, tzinfo=TZ)
DGF_ADDRESS_REQUIRED_FROM = datetime(2018, 2, 9, tzinfo=TZ)

DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE = "propertyLease"

VIEW_LOCATIONS = [
    "openprocurement.auctions.lease.views",
]

MANDATORY_ADDITIONAL_CLASSIFICATOR = {'scheme': u'CPVS', 'id': u'PA01-7', 'description': u'Оренда'}

DEFAULT_LEVEL_OF_ACCREDITATION = {'create': [1],
                                  'edit': [2]}
