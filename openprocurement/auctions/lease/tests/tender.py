# -*- coding: utf-8 -*-
import re
import unittest
# from calendar import monthrange
# from copy import deepcopy
# from datetime import datetime, timedelta, time, date
# from uuid import uuid4
# from iso8601 import parse_date
# import pytz

from openprocurement.auctions.lease.models import propertyLease
from openprocurement.auctions.lease.tests.base import test_auction_maximum_data, test_auction_data, test_financial_auction_data, test_organization, test_financial_organization, BaseWebTest, BaseAuctionWebTest, DEFAULT_ACCELERATION, test_bids, test_financial_bids

from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.core.tests.blanks.tender_blanks import (
    simple_add_auction
)
from openprocurement.auctions.core.tests.blanks.tender_blanks import (
    # AuctionResourceTest
    auction_features_invalid,
    auction_features,
    patch_tender_jsonpatch,
    dateModified_auction,
    guarantee,
    empty_listing,
    listing,
    listing_changes,
    listing_draft,
    create_auction_draft,
    get_auction,
    auction_not_found,
    invalid_auction_conditions
)
from openprocurement.auctions.lease.tests.blanks.tender_blanks import (
    # AuctionTest
    create_role,
    edit_role,
    # AuctionResourceTest
    create_auction_validation_accelerated,
    create_auction_invalid,
    required_dgf_id,
    required_dgf_item_address,
    create_auction_auctionPeriod,
    create_auction_rectificationPeriod_generated,
    create_auction_rectificationPeriod_set,
    create_auction_generated,
    create_auction,
    additionalClassifications,
    cavps_cpvs_classifications,
    patch_auction,
    patch_auction_rectificationPeriod_invalidationDate,
    patch_old_auction_rectificationPeriod_invalidationDate,
    auction_Administrator_change,
    # AuctionFieldsEditingTest
    patch_auction_denied,
    patch_auction_during_rectification_period,
    invalidate_bids_auction_unsuccessful,
    # AuctionProcessTest
    one_valid_bid_auction,
    one_invalid_bid_auction,
    first_bid_auction
)


class AuctionTest(BaseWebTest):
    auction = propertyLease
    initial_data = test_auction_data
    test_simple_add_auction = snitch(simple_add_auction)
    test_create_role = snitch(create_role)
    test_edit_role = snitch(edit_role)


class AuctionResourceTest(BaseWebTest):
    initial_data = test_auction_data
    initial_organization = test_organization
    initial_status = 'active.tendering'

    test_empty_listing = snitch(empty_listing)
    test_listing = snitch(listing)
    test_listing_changes = snitch(listing_changes)
    test_listing_draft = snitch(listing_draft)
    test_create_auction_draft = snitch(create_auction_draft)
    test_get_auction = snitch(get_auction)
    test_auction_not_found = snitch(auction_not_found)
    test_create_auction_validation_accelerated = snitch(create_auction_validation_accelerated)
    test_create_auction_invalid = snitch(create_auction_invalid)
    test_required_dgf_id = snitch(required_dgf_id)
    test_required_dgf_item_address = snitch(required_dgf_item_address)
    test_create_auction_auctionPeriod = snitch(create_auction_auctionPeriod)
    test_create_auction_rectificationPeriod_generated = snitch(create_auction_rectificationPeriod_generated)
    test_create_auction_rectificationPeriod_set = snitch(create_auction_rectificationPeriod_set)
    test_create_auction_generated = snitch(create_auction_generated)
    test_create_auction = snitch(create_auction)
    test_additionalClassifications = snitch(additionalClassifications)
    test_cavps_cpvs_classifications = snitch(cavps_cpvs_classifications)
    test_auction_features_invalid = snitch(unittest.skip("option not available")(auction_features_invalid))
    test_auction_features = snitch(unittest.skip("option not available")(auction_features))
    test_patch_tender_jsonpatch = snitch(patch_tender_jsonpatch)
    test_patch_auction = snitch(patch_auction)
    test_patch_auction_rectificationPeriod_invalidationDate = snitch(patch_auction_rectificationPeriod_invalidationDate)
    test_patch_old_auction_rectificationPeriod_invalidationDate = snitch(patch_old_auction_rectificationPeriod_invalidationDate)
    test_dateModified_auction = snitch(dateModified_auction)
    test_guarantee = snitch(guarantee)
    test_auction_Administrator_change = snitch(auction_Administrator_change)


class AuctionFieldsEditingTest(BaseAuctionWebTest):
    initial_data = test_auction_data
    initial_maximum_data = test_auction_maximum_data
    initial_organization = test_organization
    initial_bids = test_bids
    patch_auction_denied = snitch(patch_auction_denied)
    patch_auction_during_rectification_period = snitch(patch_auction_during_rectification_period)
    invalidate_bids_auction_unsuccessful = snitch(invalidate_bids_auction_unsuccessful)


class AuctionProcessTest(BaseAuctionWebTest):
    test_invalid_auction_conditions = snitch(unittest.skip("option not available")(invalid_auction_conditions))
    test_one_valid_bid_auction = snitch(one_valid_bid_auction)
    test_one_invalid_bid_auction = snitch(one_invalid_bid_auction)
    test_first_bid_auction = snitch(first_bid_auction)


    #setUp = BaseWebTest.setUp
    def setUp(self):
        super(AuctionProcessTest.__bases__[0], self).setUp()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionProcessTest))
    suite.addTest(unittest.makeSuite(AuctionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionFieldsEditingTest))
    suite.addTest(unittest.makeSuite(AuctionTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
