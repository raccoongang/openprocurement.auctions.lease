# -*- coding: utf-8 -*-
from datetime import timedelta
from openprocurement.auctions.core.adapters import AuctionConfigurator, AuctionManagerAdapter
from openprocurement.auctions.lease.models import (
    propertyLease
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingV2_1ConfiguratorMixin
)
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE, TZ, calculate_business_date, get_request_from_root, get_now,
)
from openprocurement.api.utils import get_now, set_specific_hour


class AuctionLeaseConfigurator(AuctionConfigurator, AwardingV2_1ConfiguratorMixin):
    name = 'Auction Lease Configurator'
    model = propertyLease


class AuctionLeaseManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        auction = request.validated['auction']
        if not auction.tenderPeriod:
            return
        workingDay_before_startDate = calculate_business_date(auction.auctionPeriod.startDate, -timedelta(days=1), auction, working_days=True)
        three_workingDays_before_startDate = calculate_business_date(workingDay_before_startDate, -timedelta(days=3), auction, working_days=True)
        if auction.tenderPeriod.endDate and set_specific_hour(auction.tenderPeriod.endDate, hour=20) == set_specific_hour(three_workingDays_before_startDate, hour=20):
                auction.tenderPeriod.endDate = set_specific_hour(auction.tenderPeriod.endDate,  hour=20)
        else:
            request.errors.add('body', 'data', 'the pause between tenderPeriod.endDate and auctionPeriod.startDate should be either 3 or 0 days')
            request.errors.status = 422


    def change_auction(self, request):
        pass
