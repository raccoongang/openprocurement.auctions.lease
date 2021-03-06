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
    TZ,
    calculate_business_date,
    generate_rectificationPeriod_tender_period_margin,
    get_now,
    get_request_from_root,
)
from openprocurement.api.utils import (
    set_specific_hour,
)
from .constants import MANDATORY_ADDITIONAL_CLASSIFICATOR


class AuctionLeaseConfigurator(AuctionConfigurator, AwardingV2_1ConfiguratorMixin):
    name = 'Auction Lease Configurator'
    model = propertyLease


class AuctionLeaseManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        auction = request.validated['auction']
        now = get_now()
        start_date = TZ.localize(auction.auctionPeriod.startDate.replace(tzinfo=None))
        pause_between_periods = start_date - (set_specific_hour(start_date, hour=20) - timedelta(days=1))
        end_date = calculate_business_date(start_date, -pause_between_periods, auction)
        if auction.tenderPeriod and auction.tenderPeriod.endDate:
            four_workingDays_before_startDate = calculate_business_date(start_date, -timedelta(days=4), auction, working_days=True, specific_hour=20)
            if auction.tenderPeriod.endDate.date() != four_workingDays_before_startDate.date():
                request.errors.add('body', 'data', 'The only possible value for tenderPeriod.endDate is {}'.format(four_workingDays_before_startDate))
                request.errors.status = 422
                return
            else:
                auction.tenderPeriod.endDate = four_workingDays_before_startDate
        else:
            auction.tenderPeriod = type(auction).tenderPeriod.model_class()
            auction.tenderPeriod.endDate = end_date
        if not auction.enquiryPeriod:
            auction.enquiryPeriod = type(auction).enquiryPeriod.model_class()
        auction.enquiryPeriod.endDate = end_date
        if not auction.rectificationPeriod:
            auction.rectificationPeriod = generate_rectificationPeriod_tender_period_margin(auction)
        auction.tenderPeriod.startDate = auction.enquiryPeriod.startDate = auction.rectificationPeriod.startDate = auction.date = now
        auction.auctionPeriod.startDate = None
        auction.auctionPeriod.endDate = None
        if auction.lots:
            for lot in auction.lots:
                lot.date = now

        mandatory_additional_classificator = type(auction).items.model_class.additionalClassifications.model_class(MANDATORY_ADDITIONAL_CLASSIFICATOR)
        for item in auction['items']:
            for additionalClassification in item['additionalClassifications']:
                if (additionalClassification['scheme'] == u'CPVS' and additionalClassification['id'] == u'PA01-7'):
                    break
            else:
                item['additionalClassifications'].append(mandatory_additional_classificator)

    def change_auction(self, request):
        pass
