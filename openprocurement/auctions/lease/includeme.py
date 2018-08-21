import os

import logging

from pyramid.interfaces import IRequest

from openprocurement.auctions.core.interfaces import IAuctionManager

from openprocurement.auctions.core.includeme import get_evenly_plugins

from openprocurement.auctions.core.includeme import (
    IContentConfigurator,
    IAwardingNextCheck
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingNextCheckV2_1
)

from openprocurement.auctions.lease.adapters import (
    AuctionLeaseConfigurator,
    AuctionLeaseManagerAdapter
)
from openprocurement.auctions.lease.constants import (
    DEFAULT_LEVEL_OF_ACCREDITATION,
    DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE,
    VIEW_LOCATIONS
)
from openprocurement.auctions.lease.models import (
    Auction,
    ILeaseAuction,
)

LOGGER = logging.getLogger(__name__)


def includeme_lease(config, plugin_map):
    procurement_method_types = plugin_map.get('aliases', [])
    if plugin_map.get('use_default', False):
        procurement_method_types.append(
            DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE
        )
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(Auction,
                                                 procurementMethodType)

    # add views
    for view_location in VIEW_LOCATIONS:
        config.scan(view_location)

    # Register adapters
    config.registry.registerAdapter(
        AuctionLeaseConfigurator,
        (ILeaseAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AwardingNextCheckV2_1,
        (ILeaseAuction,),
        IAwardingNextCheck
    )
    config.registry.registerAdapter(
        AuctionLeaseManagerAdapter,
        (ILeaseAuction, ),
        IAuctionManager
    )
    # migrate data
    if plugin_map['migration'] and not os.environ.get('MIGRATION_SKIP'):
        get_evenly_plugins(config, plugin_map['plugins'], 'openprocurement.auctions.lease.plugins')

    LOGGER.info("Included openprocurement.auctions.lease.property plugin",
                extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    if not plugin_map.get('accreditation'):
        config.registry.accreditation['auction'][Auction._internal_type] = DEFAULT_LEVEL_OF_ACCREDITATION
    else:
        config.registry.accreditation['auction'][Auction._internal_type] = plugin_map['accreditation']
