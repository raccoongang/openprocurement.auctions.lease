# -*- coding: utf-8 -*-
from datetime import timedelta
from openprocurement.auctions.core.adapters import AuctionConfigurator, AuctionManagerAdapter
from openprocurement.auctions.lease.models import (
    propertyLease,
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

        if not auction.enquiryPeriod:
            auction.enquiryPeriod = type(auction).enquiryPeriod.model_class()

        now = get_now()
        start_date = TZ.localize(auction.auctionPeriod.startDate.replace(tzinfo=None))
        pause_between_periods = start_date - (set_specific_hour(start_date, hour=20) - timedelta(days=1))
        end_date = calculate_business_date(start_date, -pause_between_periods, auction)
        auction.enquiryPeriod.startDate = now
        auction.enquiryPeriod.endDate = end_date
        if not auction.tenderPeriod:
            auction.tenderPeriod = type(auction).tenderPeriod.model_class()
            auction.tenderPeriod.startDate = now
            auction.tenderPeriod.endDate = end_date
            return
        four_workingDays_before_startDate = calculate_business_date(auction.auctionPeriod.startDate, -timedelta(days=4), auction, working_days=True, specific_hour=20)
        if auction.tenderPeriod.endDate:
            if auction.tenderPeriod.endDate.date() != four_workingDays_before_startDate.date():
                request.errors.add('body', 'data', 'the pause between tenderPeriod.endDate and auctionPeriod.startDate should be either 3 or 0 days')
                request.errors.status = 422
            else:
                auction.tenderPeriod.startDate = now
                auction.tenderPeriod.endDate = four_workingDays_before_startDate


    def change_auction(self, request):
        pass
