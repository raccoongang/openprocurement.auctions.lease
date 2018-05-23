# -*- coding: utf-8 -*-
from datetime import timedelta
from openprocurement.auctions.core.adapters import AuctionConfigurator, AuctionManagerAdapter
from openprocurement.auctions.lease.models import (
    propertyLease,
    Auction
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingV2_1ConfiguratorMixin
)
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE, TZ, calculate_business_date, get_request_from_root, get_now,
)
from openprocurement.api.utils import set_specific_hour


class AuctionLeaseConfigurator(AuctionConfigurator, AwardingV2_1ConfiguratorMixin):
    name = 'Auction Lease Configurator'
    model = propertyLease


class AuctionLeaseManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        auction = request.validated['auction']
        for item in auction['items']:
            if not [additionalClassification for additionalClassification in item['additionalClassifications'] if (additionalClassification['scheme'] == u'CPVS' and additionalClassification['id'] == u'PA01-7')]:
                item['additionalClassifications'].append({'scheme': u'CPVS', 'id': u'PA01-7', 'description': u'Property lease'})

        if not auction.tenderPeriod:
            auction.tenderPeriod = Auction.tenderPeriod.model_class()
            now = get_now()
            start_date = TZ.localize(auction.auctionPeriod.startDate.replace(tzinfo=None))
            auction.tenderPeriod.startDate = now
            pause_between_periods = start_date - (start_date.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=1))
            end_date = calculate_business_date(start_date, -pause_between_periods, auction)
            auction.tenderPeriod.endDate = end_date
            return
        four_workingDays_before_startDate = calculate_business_date(auction.auctionPeriod.startDate, -timedelta(days=4), auction, working_days=True)
        if auction.tenderPeriod.endDate:
            if auction.tenderPeriod.endDate.date() != four_workingDays_before_startDate.date():
                request.errors.add('body', 'data', 'the pause between tenderPeriod.endDate and auctionPeriod.startDate should be either 3 or 0 days')
                request.errors.status = 422
            else:
                auction.tenderPeriod.endDate = set_specific_hour(auction.tenderPeriod.endDate, hour=20)


    def change_auction(self, request):
        pass
