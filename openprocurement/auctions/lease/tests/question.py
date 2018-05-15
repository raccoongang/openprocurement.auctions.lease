# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.core.tests.question import (
    AuctionQuestionResourceTestMixin
)
from openprocurement.auctions.core.tests.blanks.question_blanks import (
    create_auction_question_lot,
    patch_auction_question_lot
)
from openprocurement.auctions.core.tests.base import snitch

from openprocurement.auctions.lease.tests.base import BaseAuctionWebTest, test_lots, test_financial_auction_data, test_financial_organization


class AuctionQuestionResourceTest(BaseAuctionWebTest, AuctionQuestionResourceTestMixin):
    pass


@unittest.skip("option not available")
class AuctionLotQuestionResourceTest(BaseAuctionWebTest):
    initial_lots = 2 * test_lots
    create_auction_question_lot = snitch(create_auction_question_lot)
    patch_auction_question_lot = snitch(patch_auction_question_lot)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AuctionQuestionResourceTest))
    suite.addTest(unittest.makeSuite(AuctionLotQuestionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
