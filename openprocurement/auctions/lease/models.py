# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from uuid import uuid4
from decimal import Decimal

from schematics.exceptions import ValidationError
from schematics.transforms import blacklist, whitelist
from schematics.types import StringType, IntType, BooleanType, MD5Type
from schematics.types.compound import ModelType
from schematics.types.serializable import serializable
from pyramid.security import Allow
from zope.interface import implementer

from openprocurement.auctions.core.includeme import IAwardingNextCheck
from openprocurement.auctions.core.models import (
    Auction as BaseAuction,
    get_auction,
    Lot,
    Period,
    Question as BaseQuestion,
    ProcuringEntity as flashProcuringEntity,
    Feature,
    validate_items_uniq,
    validate_features_uniq, validate_lots_uniq,
    schematics_embedded_role, IsoDateTimeType,
    IAuction,
    calc_auction_end_time,
    edit_role,
    Administrator_role,
    dgfCDB2Document as Document,
    dgfCDB2Item as Item,
    dgfOrganization as Organization,
    dgfCDB2Complaint as Complaint,
    Identifier,
    ListType,
    dgfCDB2CPVCAVClassification,
    dgfCDB2AdditionalClassification,
    Bid as BaseBid
)
from openprocurement.auctions.core.plugins.awarding.v2_1.models import Award
from openprocurement.auctions.core.plugins.contracting.v2_1.models import Contract
from openprocurement.auctions.core.utils import (
    SANDBOX_MODE, TZ, calculate_business_date, get_request_from_root, get_now,
    AUCTIONS_COMPLAINT_STAND_STILL_TIME as COMPLAINT_STAND_STILL_TIME
)

from openprocurement.api.models.schematics_extender import (
    Model,
    IsoDurationType,
    DecimalType
)

from openprocurement.api.models.auction_models import (
    Cancellation as BaseCancellation,
     Value as BaseVAlue
)

from .constants import (
    DGF_ID_REQUIRED_FROM,
    MINIMAL_EXPOSITION_PERIOD,
    MINIMAL_EXPOSITION_REQUIRED_FROM,
    MINIMAL_PERIOD_FROM_RECTIFICATION_END,
)
from .utils import get_auction_creation_date


def bids_validation_wrapper(validation_func):
    def validator(klass, data, value):
        orig_data = data
        while not isinstance(data['__parent__'], BaseAuction):
            # in case this validation wrapper is used for subelement of bid (such as parameters)
            # traverse back to the bid to get possibility to check status  # troo-to-to =)
            data = data['__parent__']
        if data['status'] in ('invalid', 'draft'):
            # skip not valid bids
            return
        tender = data['__parent__']
        request = tender.__parent__.request
        if request.method == "PATCH" and isinstance(tender, BaseAuction) and request.authenticated_role == "auction_owner":
            # disable bids validation on tender PATCH requests as tender bids will be invalidated
            return
        return validation_func(klass, orig_data, value)
    return validator


class ProcuringEntity(flashProcuringEntity):
    identifier = ModelType(Identifier, required=True)
    additionalIdentifiers = ListType(ModelType(Identifier))


class Bid(BaseBid):
    class Options:
        roles = {
            'create': whitelist('value', 'tenderers', 'parameters', 'lotValues', 'status', 'qualified'),
        }

    status = StringType(choices=['active', 'draft', 'invalid'], default='active')
    tenderers = ListType(ModelType(Organization), required=True, min_size=1, max_size=1)
    documents = ListType(ModelType(Document), default=list())
    qualified = BooleanType(required=True, choices=[True])

    @bids_validation_wrapper
    def validate_value(self, data, value):
        BaseBid._validator_functions['value'](self, data, value)

class Question(BaseQuestion):
    author = ModelType(Organization, required=True)


class Cancellation(BaseCancellation):
    documents = ListType(ModelType(Document), default=list())


def validate_not_available(items, *args):
    if items:
        raise ValidationError(u"Option not available in this procurementMethodType")


def rounding_shouldStartAfter(start_after, auction, use_from=datetime(2016, 6, 1, tzinfo=TZ)):
    if (auction.enquiryPeriod and auction.enquiryPeriod.startDate or get_now()) > use_from and not (SANDBOX_MODE and auction.submissionMethodDetails and u'quick' in auction.submissionMethodDetails):
        midnigth = datetime.combine(start_after.date(), time(0, tzinfo=start_after.tzinfo))
        if start_after >= midnigth:
            start_after = midnigth + timedelta(1)
    return start_after


class AuctionAuctionPeriod(Period):
    """The auction period."""

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        auction = self.__parent__
        if auction.lots or auction.status not in ['active.tendering', 'active.auction']:
            return
        if self.startDate and get_now() > calc_auction_end_time(auction.numberOfBids, self.startDate):
            start_after = calc_auction_end_time(auction.numberOfBids, self.startDate)
        elif auction.enquiryPeriod and auction.enquiryPeriod.endDate:
            start_after = auction.enquiryPeriod.endDate
        else:
            return
        return rounding_shouldStartAfter(start_after, auction).isoformat()

    def validate_startDate(self, data, startDate):
        auction = get_auction(data['__parent__'])
        if not auction.revisions and not startDate:
            raise ValidationError(u'This field is required.')

            
class RectificationPeriod(Period):
    invalidationDate = IsoDateTimeType()


create_role = (blacklist(
    'owner_token', 'transfer_token', 'owner', '_attachments', 'revisions', 'date', 'dateModified', 'doc_id', 'auctionID', 'bids',
    'documents', 'awards', 'questions', 'complaints', 'auctionUrl', 'status',
    'enquiryPeriod', 'awardPeriod', 'procurementMethod', 'eligibilityCriteria',
    'eligibilityCriteria_en', 'eligibilityCriteria_ru', 'awardCriteria', 'submissionMethod', 'cancellations',
    'numberOfBidders', 'contracts') + schematics_embedded_role)
edit_role = (edit_role + blacklist('enquiryPeriod', 'tenderPeriod', 'auction_value', 'auction_minimalStep', 'auction_guarantee', 'eligibilityCriteria', 'eligibilityCriteria_en', 'eligibilityCriteria_ru', 'awardCriteriaDetails', 'awardCriteriaDetails_en', 'awardCriteriaDetails_ru', 'procurementMethodRationale', 'procurementMethodRationale_en', 'procurementMethodRationale_ru', 'submissionMethodDetails', 'submissionMethodDetails_en', 'submissionMethodDetails_ru', 'minNumberOfQualifiedBids'))
Administrator_role = (Administrator_role + whitelist('awards'))


class ILeaseAuction(IAuction):
    """Marker interface for Lease auctions"""


class Value(BaseVAlue):
    amount = DecimalType(precision=-2, min_value=Decimal('0'))


class TaxHolidays(Model):
    id = MD5Type(required=True, default=lambda: uuid4().hex)
    taxHolidaysDuration = IsoDurationType(required=True)
    conditions = StringType(required=True)
    conditions_en = StringType()
    conditions_ru = StringType()
    value = ModelType(Value, required=True)

    def validate_value(self, data, value):
        if value.currency != u'UAH':
            raise ValidationError(u"currency should be only UAH")

    # def validate_value(self, data, value):
        # BaseBid._validator_functions['value'](self, data, value)

class EscalationClauses(Model):
    id = MD5Type(required=True, default=lambda: uuid4().hex)
    escalationPeriodicity = IsoDurationType(required=True)
    escalationStepPercentageRange = DecimalType(required=True, precision=-3, min_value=Decimal('0'), max_value=Decimal('1.000'))
    conditions = StringType(required=True)
    conditions_en = StringType()
    conditions_ru = StringType()


class PropertyLeaseClassification(dgfCDB2CPVCAVClassification):
    scheme = StringType(required=True, choices=[u'CAV-PS'])


class PropertyItem(Item):
    """A property item to be leased."""
    classification = ModelType(PropertyLeaseClassification, required=True)


class LeaseTerms(Model):

    leaseDuration = IsoDurationType(required=True)
    taxHolidays = ListType(ModelType(TaxHolidays))
    escalationClauses = ListType(ModelType(EscalationClauses))

class ContractTerms(Model):

    contractType = StringType(required=True, choices=['lease'])
    leaseTerms = ModelType(LeaseTerms, required=True)


@implementer(ILeaseAuction)
class Auction(BaseAuction):
    """Data regarding auction process - publicly inviting prospective contractors to submit bids for evaluation and selecting a winner or winners."""
    class Options:
        roles = {
            'create': create_role,
            'edit_active.tendering': (blacklist('enquiryPeriod', 'tenderPeriod', 'rectificationPeriod', 'auction_value', 'auction_minimalStep', 'auction_guarantee', 'eligibilityCriteria', 'eligibilityCriteria_en', 'eligibilityCriteria_ru', 'minNumberOfQualifiedBids', 'contractTerms') + edit_role),
            'Administrator': (whitelist('rectificationPeriod') + Administrator_role),
        }

    _procedure_type = "propertyLease"
    awards = ListType(ModelType(Award), default=list())
    bids = ListType(ModelType(Bid), default=list())  # A list of all the companies who entered submissions for the auction.
    cancellations = ListType(ModelType(Cancellation), default=list())
    complaints = ListType(ModelType(Complaint), default=list())
    contracts = ListType(ModelType(Contract), default=list())
    dgfID = StringType()
    documents = ListType(ModelType(Document), default=list())  # All documents and attachments related to the auction.
    enquiryPeriod = ModelType(Period)  # The period during which enquiries may be made and will be answered.
    rectificationPeriod = ModelType(RectificationPeriod)  # The period during which editing of main procedure fields are allowed
    tenderPeriod = ModelType(Period)  # The period when the auction is open for submissions. The end date is the closing date for auction submissions.
    tenderAttempts = IntType(choices=[1, 2, 3, 4])
    auctionPeriod = ModelType(AuctionAuctionPeriod, required=True, default={})
    procurementMethodType = StringType()
    procuringEntity = ModelType(ProcuringEntity, required=True)
    status = StringType(choices=['draft', 'active.tendering', 'active.auction', 'active.qualification', 'active.awarded', 'complete', 'cancelled', 'unsuccessful'], default='active.tendering')
    questions = ListType(ModelType(Question), default=list())
    features = ListType(ModelType(Feature), validators=[validate_features_uniq, validate_not_available])
    lots = ListType(ModelType(Lot), default=list(), validators=[validate_lots_uniq, validate_not_available])
    items = ListType(ModelType(PropertyItem), required=True, min_size=1, validators=[validate_items_uniq])
    minNumberOfQualifiedBids = IntType(choices=[1, 2])
    contractTerms = ModelType(ContractTerms, required=True)

    def __acl__(self):
        return [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_auction'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_auction_award'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_auction_documents'),
        ]

    def initialize(self): # TODO: get rid of this method
        pass

    def validate_tenderPeriod(self, data, period):
        if not (period and period.startDate and period.endDate):
            return
        if get_auction_creation_date(data) < MINIMAL_EXPOSITION_REQUIRED_FROM:
            return
        if calculate_business_date(period.startDate, MINIMAL_EXPOSITION_PERIOD, data) > period.endDate:
            raise ValidationError(u"tenderPeriod should be greater than 6 days")

    def validate_rectificationPeriod(self, data, period):
        if not (period and period.startDate) or not period.endDate:
            return
        if period.endDate > TZ.localize(calculate_business_date(data['tenderPeriod']['endDate'], -MINIMAL_PERIOD_FROM_RECTIFICATION_END, data).replace(tzinfo=None)):
            raise ValidationError(u"rectificationPeriod.endDate should come at least 5 working days earlier than tenderPeriod.endDate")

    def validate_value(self, data, value):
        if value.currency != u'UAH':
            raise ValidationError(u"currency should be only UAH")

    def validate_dgfID(self, data, dgfID):
        if not dgfID:
            if get_auction_creation_date(data) > DGF_ID_REQUIRED_FROM:
                raise ValidationError(u'This field is required.')

    @serializable(serialize_when_none=False)
    def next_check(self):
        now = get_now()
        checks = []
        if self.status == 'active.tendering' and self.tenderPeriod and self.tenderPeriod.endDate:
            checks.append(self.tenderPeriod.endDate.astimezone(TZ))
        elif not self.lots and self.status == 'active.auction' and self.auctionPeriod and self.auctionPeriod.startDate and not self.auctionPeriod.endDate:
            if now < self.auctionPeriod.startDate:
                checks.append(self.auctionPeriod.startDate.astimezone(TZ))
            elif now < calc_auction_end_time(self.numberOfBids, self.auctionPeriod.startDate).astimezone(TZ):
                checks.append(calc_auction_end_time(self.numberOfBids, self.auctionPeriod.startDate).astimezone(TZ))
        elif self.lots and self.status == 'active.auction':
            for lot in self.lots:
                if lot.status != 'active' or not lot.auctionPeriod or not lot.auctionPeriod.startDate or lot.auctionPeriod.endDate:
                    continue
                if now < lot.auctionPeriod.startDate:
                    checks.append(lot.auctionPeriod.startDate.astimezone(TZ))
                elif now < calc_auction_end_time(lot.numberOfBids, lot.auctionPeriod.startDate).astimezone(TZ):
                    checks.append(calc_auction_end_time(lot.numberOfBids, lot.auctionPeriod.startDate).astimezone(TZ))
        # Use next_check part from awarding
        request = get_request_from_root(self)
        if request is not None:
            awarding_check = request.registry.getAdapter(self, IAwardingNextCheck).add_awarding_checks(self)
            if awarding_check is not None:
                checks.append(awarding_check)
        if self.status.startswith('active'):
            from openprocurement.auctions.core.utils import calculate_business_date
            for complaint in self.complaints:
                if complaint.status == 'claim' and complaint.dateSubmitted:
                    checks.append(calculate_business_date(complaint.dateSubmitted, COMPLAINT_STAND_STILL_TIME, self))
                elif complaint.status == 'answered' and complaint.dateAnswered:
                    checks.append(calculate_business_date(complaint.dateAnswered, COMPLAINT_STAND_STILL_TIME, self))
            for award in self.awards:
                for complaint in award.complaints:
                    if complaint.status == 'claim' and complaint.dateSubmitted:
                        checks.append(calculate_business_date(complaint.dateSubmitted, COMPLAINT_STAND_STILL_TIME, self))
                    elif complaint.status == 'answered' and complaint.dateAnswered:
                        checks.append(calculate_business_date(complaint.dateAnswered, COMPLAINT_STAND_STILL_TIME, self))
        return min(checks).isoformat() if checks else None


propertyLease = Auction
