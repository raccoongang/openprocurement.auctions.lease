# -*- coding: utf-8 -*-
from logging import getLogger

from pkg_resources import get_distribution

from openprocurement.auctions.core.utils import (
    API_DOCUMENT_BLACKLISTED_FIELDS as DOCUMENT_BLACKLISTED_FIELDS,
    TZ,
    check_auction_status,
    check_complaint_status,
    context_unpack,
    get_file as base_get_file,
    get_now,
    remove_draft_bids,
    log_auction_status_change,
    upload_file as base_upload_file
)

from .constants import (
    DOCUMENT_TYPE_URL_ONLY,
    DOCUMENT_TYPE_OFFLINE,
    MANDATORY_ADDITIONAL_CLASSIFICATOR
)
from openprocurement.auctions.core.interfaces import IAuctionManager


PKG = get_distribution(__package__)
LOGGER = getLogger(PKG.project_name)


def upload_file(request, blacklisted_fields=DOCUMENT_BLACKLISTED_FIELDS):
    first_document = request.validated['documents'][0] if 'documents' in request.validated and request.validated['documents'] else None
    if 'data' in request.validated and request.validated['data']:
        document = request.validated['document']
        if document.documentType in (DOCUMENT_TYPE_URL_ONLY + DOCUMENT_TYPE_OFFLINE):
            if first_document:
                for attr_name in type(first_document)._fields:
                    if attr_name not in blacklisted_fields:
                        setattr(document, attr_name, getattr(first_document, attr_name))
            if document.documentType in DOCUMENT_TYPE_OFFLINE:
                document.format = 'offline/on-site-examination'
            return document
    return base_upload_file(request, blacklisted_fields)


def get_file(request):
    document = request.validated['document']
    if document.documentType == 'virtualDataRoom':
        request.response.status = '302 Moved Temporarily'
        request.response.location = document.url
        return document.url
    return base_get_file(request)


def check_bids(request):
    auction = request.validated['auction']
    adapter = request.registry.getAdapter(auction, IAuctionManager)
    if auction.auctionPeriod:
        if auction.numberOfBids < (auction.minNumberOfQualifiedBids or 2):
            auction.auctionPeriod.startDate = None
            adapter.pendify_auction_status('unsuccessful')
        elif auction.numberOfBids == 1:
            auction.auctionPeriod.startDate = None
            request.content_configurator.start_awarding()


def check_status(request):
    auction = request.validated['auction']
    now = get_now()
    for complaint in auction.complaints:
        check_complaint_status(request, complaint, now)
    for award in auction.awards:
        for complaint in award.complaints:
            check_complaint_status(request, complaint, now)
    if not auction.lots and auction.status == 'active.tendering' and auction.tenderPeriod.endDate <= now:
        auction.status = 'active.auction'
        remove_draft_bids(request)
        remove_invalid_bids(request)
        check_bids(request)
        log_auction_status_change(request, auction, auction.status)
        return True
    elif auction.lots and auction.status == 'active.tendering' and auction.tenderPeriod.endDate <= now:
        auction.status = 'active.auction'
        remove_draft_bids(request)
        remove_invalid_bids(request)
        check_bids(request)
        [setattr(i.auctionPeriod, 'startDate', None) for i in auction.lots if i.numberOfBids < 2 and i.auctionPeriod]
        log_auction_status_change(request, auction, auction.status)
        return True
    elif not auction.lots and auction.status == 'active.awarded':
        standStillEnds = [
            a.complaintPeriod.endDate.astimezone(TZ)
            for a in auction.awards
            if a.complaintPeriod.endDate
        ]
        if not standStillEnds:
            return
        standStillEnd = max(standStillEnds)
        if standStillEnd <= now:
            check_auction_status(request)
    elif auction.lots and auction.status in ['active.qualification', 'active.awarded']:
        if any([i['status'] in auction.block_complaint_status and i.relatedLot is None for i in auction.complaints]):
            return
        for lot in auction.lots:
            if lot['status'] != 'active':
                continue
            lot_awards = [i for i in auction.awards if i.lotID == lot.id]
            standStillEnds = [
                a.complaintPeriod.endDate.astimezone(TZ)
                for a in lot_awards
                if a.complaintPeriod.endDate
            ]
            if not standStillEnds:
                continue
            standStillEnd = max(standStillEnds)
            if standStillEnd <= now:
                check_auction_status(request)
                return


def get_auction_creation_date(data):
    auction_creation_date = (data.get('revisions')[0].date if data.get('revisions') else get_now())
    return auction_creation_date


def remove_invalid_bids(request):
    auction = request.validated['auction']
    if [bid for bid in auction.bids if getattr(bid, "status", "active") == "invalid"]:
        LOGGER.info('Remove invalid bids',
                    extra=context_unpack(request, {'MESSAGE_ID': 'remove_invalid_bids'}))
        auction.bids = [bid for bid in auction.bids if getattr(bid, "status", "active") != "invalid"]


def invalidate_bids_data(auction):
    for bid in auction.bids:
        setattr(bid, "status", "invalid")
    auction.rectificationPeriod.invalidationDate = get_now()


def append_additional_classificator(auction):
    mandatory_additional_classificator = type(auction).items.model_class.additionalClassifications.model_class(
        MANDATORY_ADDITIONAL_CLASSIFICATOR)
    for item in auction['items']:
        for additionalClassification in item['additionalClassifications']:
            if (additionalClassification['scheme'] == MANDATORY_ADDITIONAL_CLASSIFICATOR['scheme'] and additionalClassification['id'] == MANDATORY_ADDITIONAL_CLASSIFICATOR['id']):
                break
        else:
            item['additionalClassifications'].append(mandatory_additional_classificator)
