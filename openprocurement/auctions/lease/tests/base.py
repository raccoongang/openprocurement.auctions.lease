# -*- coding: utf-8 -*-
import os
from base64 import b64encode
from copy import deepcopy
from datetime import datetime, timedelta
from urllib import urlencode
from uuid import uuid4

from openprocurement.auctions.core.tests.base import (
    BaseWebTest as CoreBaseWebTest,
    BaseAuctionWebTest as CoreBaseAuctionWebTest,
    MOCK_CONFIG as BASE_MOCK_CONFIG
)
from openprocurement.auctions.core.utils import (
    apply_data_patch,
    get_now,
    SANDBOX_MODE,
    connection_mock_config
)

from openprocurement.auctions.lease.tests.fixtures import PARTIAL_MOCK_CONFIG

from openprocurement.auctions.lease.constants import (
    DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE
)

DEFAULT_ACCELERATION = 1440


now = datetime.now()
test_organization = {
    "name": u"Державне управління справами",
    "identifier": {
        "scheme": u"UA-EDR",
        "id": u"00037256",
        "uri": u"http://www.dus.gov.ua/"
    },
    "address": {
        "countryName": u"Україна",
        "postalCode": u"01220",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова, 11, корпус 1"
    },
    "contactPoint": {
        "name": u"Державне управління справами",
        "telephone": u"0440000000"
    }
}
test_procuringEntity = test_organization.copy()
test_auction_data = {
    "title": u"футляри до державних нагород",
    "lotIdentifier": u"219560",
    "tenderAttempts": 1,
    "procuringEntity": test_procuringEntity,
    "value": {
        "amount": 100,
        "currency": u"UAH"
    },
    "minimalStep": {
        "amount": 35,
        "currency": u"UAH"
    },
    "contractTerms": {
        "type": "lease",
        "leaseTerms": {
            "leaseDuration": "P10Y",
            "taxHolidays": [
            {
                "taxHolidaysDuration": "P5M",
                "conditions": "conditions description",
                "value": {
                    "amount": 100.0,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ],
        "escalationClauses": [
            {
                "escalationPeriodicity": "P5M",
                "escalationStepPercentage": 0.1,
                "conditions": "conditions description"
            }
        ]
        }
    },
    "items": [
        {
            "description": u"Земля для військовослужбовців",
            "classification": {
                "scheme": "CAV-PS",
                "id": "04121000-2",
                "description": "Земельні ділянки"
            },
            "additionalClassifications": [{
                "scheme": "CPVS",
                "id": "PA01-7",
                "description": "This field is required."
            }],
            "unit": {
                "name": u"item",
                "code": u"44617100-9"
            },
            "quantity": 5.001,
            "contractPeriod": {
                "startDate": (now + timedelta(days=2)).isoformat(),
                "endDate": (now + timedelta(days=5)).isoformat()
            },
            "address": {
                "countryName": u"Україна",
                "postalCode": "79000",
                "region": u"м. Київ",
                "locality": u"м. Київ",
                "streetAddress": u"вул. Банкова 1"
            }
        }
    ],
    "auctionPeriod": {
        "startDate": (now.date() + timedelta(days=14)).isoformat()
    },
    "procurementMethodType": DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE,
}
if SANDBOX_MODE:
    test_auction_data['procurementMethodDetails'] = 'quick, accelerator={}'.format(DEFAULT_ACCELERATION)
test_auction_maximum_data = deepcopy(test_auction_data)
test_auction_maximum_data.update({
    "title_en" : u"Cases with state awards",
    "title_ru" : u"футляры к государственным наградам",
    "description" : u"футляри до державних нагород",
    "description_en" : u"Cases with state awards",
    "description_ru" : u"футляры к государственным наградам"
})
test_auction_maximum_data["items"][0].update({
    "description_en" : u"Cases with state awards",
    "description_ru" : u"футляры к государственным наградам"
})
test_features_auction_data = test_auction_data.copy()
test_features_item = test_features_auction_data['items'][0].copy()
test_features_item['id'] = "1"
test_features_auction_data['items'] = [test_features_item]
test_features_auction_data["features"] = [
    {
        "code": "OCDS-123454-AIR-INTAKE",
        "featureOf": "item",
        "relatedItem": "1",
        "title": u"Потужність всмоктування",
        "title_en": "Air Intake",
        "description": u"Ефективна потужність всмоктування пилососа, в ватах (аероватах)",
        "enum": [
            {
                "value": 0.1,
                "title": u"До 1000 Вт"
            },
            {
                "value": 0.15,
                "title": u"Більше 1000 Вт"
            }
        ]
    },
    {
        "code": "OCDS-123454-YEARS",
        "featureOf": "tenderer",
        "title": u"Років на ринку",
        "title_en": "Years trading",
        "description": u"Кількість років, які організація учасник працює на ринку",
        "enum": [
            {
                "value": 0.05,
                "title": u"До 3 років"
            },
            {
                "value": 0.1,
                "title": u"Більше 3 років, менше 5 років"
            },
            {
                "value": 0.15,
                "title": u"Більше 5 років"
            }
        ]
    }
]
base_test_bids = [
    {
        "tenderers": [
            test_organization
        ],
        "value": {
            "amount": 469,
            "currency": "UAH",
            "valueAddedTaxIncluded": True
        }
    },
    {
        "tenderers": [
            test_organization
        ],
        "value": {
            "amount": 479,
            "currency": "UAH",
            "valueAddedTaxIncluded": True
        }
    }
]

test_bids = []
for i in base_test_bids:
    i = deepcopy(i)
    i.update({'qualified': True})
    test_bids.append(i)

test_lots = [
    {
        'title': 'lot title',
        'description': 'lot description',
        'value': test_auction_data['value'],
        'minimalStep': test_auction_data['minimalStep'],
    }
]
test_features = [
    {
        "code": "code_item",
        "featureOf": "item",
        "relatedItem": "1",
        "title": u"item feature",
        "enum": [
            {
                "value": 0.01,
                "title": u"good"
            },
            {
                "value": 0.02,
                "title": u"best"
            }
        ]
    },
    {
        "code": "code_tenderer",
        "featureOf": "tenderer",
        "title": u"tenderer feature",
        "enum": [
            {
                "value": 0.01,
                "title": u"good"
            },
            {
                "value": 0.02,
                "title": u"best"
            }
        ]
    }
]

test_financial_auction_data = deepcopy(test_auction_data)
test_financial_auction_data["procurementMethodType"] = DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE

test_financial_organization = deepcopy(test_organization)
test_financial_organization['additionalIdentifiers'] = [{
    "scheme": u"UA-FIN",
    "id": u"А01 457213"
}]

test_financial_bids = []
for i in test_bids:
    bid = deepcopy(i)
    bid.update({'eligible': True})
    bid['tenderers'] = [test_financial_organization]
    test_financial_bids.append(bid)


MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'auctions.core', 'plugins'))


class BaseWebTest(CoreBaseWebTest):

    """Base Web Test to test openprocurement.auctions.lease.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)
    mock_config = MOCK_CONFIG


class BaseAuctionWebTest(CoreBaseAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_auction_data
    initial_organization = test_organization
    mock_config = MOCK_CONFIG

    def go_to_rectificationPeriod_end(self):
        now = get_now()
        self.set_status('active.tendering', {
            "rectificationPeriod": {
                "startDate": (now - timedelta(days=14)).isoformat(),
                "endDate": (now - (timedelta(minutes=6) if SANDBOX_MODE else timedelta(days=6))).isoformat()
            },
            "tenderPeriod": {
                "startDate": (now - timedelta(days=14)).isoformat(),
                "endDate": (now + (timedelta(minutes=1) if SANDBOX_MODE else timedelta(days=1))).isoformat()
            },
            "enquiryPeriod": {
                "startDate": (now - timedelta(days=14)).isoformat(),
                "endDate": (now + (timedelta(minutes=1) if SANDBOX_MODE else timedelta(days=1))).isoformat()
            },
            "auctionPeriod": {
                "startDate": (now + timedelta(days=1)).isoformat()
            }
        })

    def set_status(self, status, extra=None):
        data = {'status': status}
        if status == 'active.tendering':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=7)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=1)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=7)).isoformat()
                }
            })
        elif status == 'active.auction':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=7)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=7)).isoformat(),
                    "endDate": (now - timedelta(days=6)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=7)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=6)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.awarded':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=6)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'complete':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=18)).isoformat(),
                    "endDate": (now - timedelta(days=11)).isoformat()
                },
                "rectificationPeriod": {
                    "startDate": (now - timedelta(days=18)).isoformat(),
                    "endDate": (now - timedelta(days=17)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=18)).isoformat(),
                    "endDate": (now - timedelta(days=11)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=11)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=10)).isoformat(),
                    "endDate": (now - timedelta(days=10)).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=11)).isoformat(),
                                "endDate": (now - timedelta(days=10)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        if extra:
            data.update(extra)
        auction = self.db.get(self.auction_id)
        auction.update(apply_data_patch(auction, data))
        self.db.save(auction)
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        #response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.app.authorization = authorization
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response

    def upload_auction_protocol(self, award):
        award_id = award['id']
        response = self.app.post_json('/auctions/{}/awards/{}/documents?acc_token={}'.format(self.auction_id, award_id, self.auction_token),
            {'data': {
                'title': 'auction_protocol.pdf',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
                "description": "auction protocol",
                "documentType": 'auctionProtocol',

            }})

        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('auction_protocol.pdf', response.json["data"]["title"])
        self.assertEqual('auctionProtocol', response.json["data"]["documentType"])
        self.assertEqual('auction_owner', response.json["data"]["author"])

    def post_auction_results(self):
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": b['value']
                }
                for i, b in enumerate(self.initial_bids)
            ]
        }
        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    def generate_docservice_url(self):
        uuid = uuid4().hex
        key = self.app.app.registry.docservice_key
        keyid = key.hex_vk()[:8]
        signature = b64encode(key.signature("{}\0{}".format(uuid, '0' * 32)))
        query = {'Signature': signature, 'KeyID': keyid}
        return "http://localhost/get/{}?{}".format(uuid, urlencode(query))

    def check_award_status(self, auction_id, award_id, target_status):
        response = self.app.get(
            '/auctions/{0}/awards/{1}'.format(
                auction_id,
                award_id))
        current_status = response.json['data']['status']
        self.assertEqual(
            current_status,
            target_status,
            "Award status {0} isn't expected. Current status: {1}".format(
                current_status,
                target_status))

    def patch_award(self, award_id, status, bid_token=None):
        token = self.auction_token
        if bid_token:
            token = bid_token
        response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, award_id, token
        ), {"data": {"status": status}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response

    def forbidden_patch_award(self, award_id, before_status, status):
        response = self.app.patch_json('/auctions/{}/awards/{}?acc_token={}'.format(
            self.auction_id, award_id, self.auction_token
        ), {"data": {"status": status}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't switch award ({}) status to ({}) status".format(before_status, status))


class BaseFinancialAuctionWebTest(BaseAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_financial_auction_data
    initial_organization = test_financial_organization
