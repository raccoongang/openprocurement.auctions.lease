.. index:: Bid, Parameter, LotValue, bidder, participant, pretendent

.. _Bid:

Bid
===

Schema
------

:status:
    string, default='active'

    Possible values are:

    * `draft`
    * `active`

:tenderers:
    List of :ref:`Organization` objects, required

:documents:
    List of :ref:`Document` objects

:qualified:
    bool, required

:date:
    string, :ref:`Date`, auto-generated

    Date when bid has been submitted.

:id:
    UID, auto-generated

:status:
    string

    Possible values are:

    * `draft`
    * `active`

:value:
    :ref:`Value`, required

    Validation rules:

    * ``amount`` should be less than ``Auction.value.amout``
    * ``currency`` should either be absent or match ``Auction.value.currency``
    * ``valueAddedTaxIncluded`` should either be absent or match ``Auction.value.valueAddedTaxIncluded``

:parameters:
    List of :ref:`Parameter` objects

.. :lotValues:
    List of :ref:`LotValue` objects

:participationUrl:
    URL

    A web address for participation in auction.

:eligible:
    bool

.. _Parameter:

Parameter
=========

Schema
------

:code:
    string, required

    Feature code.

:value:
    float, required

    Feature value.

.. _LotValue:

.. LotValue
   ========

   Schema
   ------

:value:
    :ref:`Value`, required

    Validation rules:

    * `amount` should be less than `Lot.value.amout`
    * `currency` should either be absent or match `Lot.value.currency`
    * `valueAddedTaxIncluded` should either be absent or match `Lot.value.valueAddedTaxIncluded`

:relatedLot:
    string

    ID of related :ref:`Lot`.

:date:
    string, :ref:`Date`, auto-generated

:participationUrl:
    URL

    A web address for participation in auction.
