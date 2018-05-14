import logging

from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import (
    IContentConfigurator,
    IAwardingNextCheck
)
from openprocurement.auctions.core.plugins.awarding.v2_1.adapters import (
    AwardingNextCheckV2_1
)

from openprocurement.auctions.lease.adapters import (
    AuctionRubbleOtherConfigurator
)
from openprocurement.auctions.lease.constants import (
    DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE
)
from openprocurement.auctions.lease.models import (
    IRubbleAuction,
    propertyLease
)

LOGGER = logging.getLogger(__name__)


def includeme_lease(config, plugin_config=None):
    procurement_method_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        procurement_method_types.append(
            DEFAULT_PROCUREMENT_METHOD_TYPE_LEASE
        )
    for procurementMethodType in procurement_method_types:
        config.add_auction_procurementMethodType(propertyLease,
                                                 procurementMethodType)

    config.scan("openprocurement.auctions.lease.views.property")

    # Register adapters
    config.registry.registerAdapter(
        AuctionRubbleOtherConfigurator,
        (IRubbleAuction, IRequest),
        IContentConfigurator
    )
    config.registry.registerAdapter(
        AwardingNextCheckV2_1,
        (IRubbleAuction,),
        IAwardingNextCheck
    )

    LOGGER.info("Included openprocurement.auctions.lease.property plugin",
                extra={'MESSAGE_ID': 'included_plugin'})

