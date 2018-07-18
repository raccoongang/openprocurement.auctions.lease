.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Auction, Auction
.. _auction:

Auction
=======

Schema
------

:title:
   string, multilingual, required, editable during rectificationPeriod

   Auction title.

:description:
   string, multilingual, required, editable during rectificationPeriod

   Detailed auction description.

:auctionID:
   string, auto-generated, read-only

   The auction identifier to refer auction to in "paper" documentation. 

   |ocdsDescription|
   AuctionID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
   
:lotIdentifier:
    string, required, editable during rectificationPeriod
    
    Identification number of the auction (also referred to as `lot`) within the paper documentation.

   
:procuringEntity:
   :ref:`ProcuringEntity`, required

   Organization conducting the auction.
   

   |ocdsDescription|
   The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

   
:value:
   :ref:`value`, required, editable during rectificationPeriod

   Total available auction budget. Bids lower than ``value`` will be rejected.

   |ocdsDescription|
   The total estimated value of the procurement.

:guarantee:
    :ref:`Guarantee`, optional, editable during rectificationPeriod

    Bid guarantee

:items:
   list of :ref:`item` objects, required, editable during rectificationPeriod

   List that contains single item being sold. 

   |ocdsDescription|
   The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.

:features:
   list of :ref:`Feature` objects

   Features of auction.

:documents:
   List of :ref:`document` objects
 
   |ocdsDescription|
   All documents and attachments related to the auction.

:questions:
   List of :ref:`question` objects

   Questions to ``procuringEntity`` and answers to them.

:complaints:
   List of :ref:`complaint` objects

   Complaints to auction conditions and their resolutions.

:bids:
   List of :ref:`bid` objects

   A list of all bids placed in the auction with information about participants, their proposals and other qualification documentation.

   |ocdsDescription|
   A list of all the companies who entered submissions for the auction.

:minNumberOfQualifiedBids:
   integer, optional
   
   The field that indicates the minimal number of qualified bids. The possible values for the field are 1 or 2.
   
   In case of the field has been remained blank, the workflow will be similar to the auction with 2 bids.
   
   You can also fill in the field, assigning the value "1". This will show that the only one bidder is needed 
   for the procedure to be successful. Therewith the auction is omitted and that bid turns to a qualified award.
   
:minimalStep:
   :ref:`value`, required, editable during rectificationPeriod

   The minimal step of auction. Validation rules:

   * `amount` should be greater than `Auction.value.amount`
   * `currency` should either be absent or match `Auction.value.currency`
   * `valueAddedTaxIncluded` should either be absent or match `Auction.value.valueAddedTaxIncluded`

:awards:
    List of :ref:`award` objects

    All qualifications (disqualifications and awards).

:contracts:
    List of :ref:`contract` objects

:enquiryPeriod:
   :ref:`period`

   Period when questions are allowed.

   |ocdsDescription|
   The period during which enquiries may be made and will be answered.

:tenderPeriod:
   :ref:`period`

   Period when bids can be submitted.

   |ocdsDescription|
   The period when the auction is open for submissions. The end date is the closing date for auction submissions.

:auctionPeriod:
   :ref:`period`, required

   Period when Auction is conducted. `startDate` should be provided.

:auctionUrl:
    url

    A web address where auction is accessible for view.

:awardPeriod:
   :ref:`period`, read-only

   Awarding process period.

   |ocdsDescription|
   The date or period on which an award is anticipated to be made.

:status:
   string

   :`active.tendering`:
       Tendering period (tendering)
   :`active.auction`:
       Auction period (auction)
   :`active.qualification`:
       Winner qualification (qualification)
   :`active.awarded`:
       Standstill period (standstill)
   :`unsuccessful`:
       Unsuccessful auction (unsuccessful)
   :`complete`:
       Complete auction (complete)
   :`cancelled`:
       Cancelled auction (cancelled)

   Auction status.

.. :lots:
   List of :ref:`lot` objects.

   Contains all auction lots.

:cancellations:
   List of :ref:`cancellation` objects.

   Contains 1 object with `active` status in case of cancelled Auction.

   The :ref:`cancellation` object describes the reason of auction cancellation and contains accompanying
   documents  if there are any.

:revisions:
   List of :ref:`revision` objects, auto-generated

   Historical changes to `Auction` object properties.

ContractTerms
=============

Schema
------

:Type:
    string, required

    The only value for this field is ``lease``.

:leaseTerms:
    :ref:`LeaseTerms`

    The details of how property is to be leased.

.. _LeaseTerms:

LeaseTerms
==========

Schema
------

:leaseDuration:
    `ISO8601 duration`_ object, required

    The time span during which a contracted lease is in place.

:taxHolidays:
    list of :ref:`TaxHolidays`, optional

    The period during which tax concessions are made for some reason.

:escalationClauses:
    list of :ref:`EscalationClauses`, optional

    The rules for the way of monthly payment to be changed on a periodic basis.

.. _TaxHolidays:

TaxHolidays
===========

Schema
------

:taxHolidaysDuration:
    `ISO8601 duration`_ object, required

    Duration of the period within which a person or company is allowed to pay less than usual (or provide no payment).

:conditions:
    string, required, multilingual

    The details for the way of lease holidays to be held.

:value:
    :ref:`Value` object, required

    The amount to be paid by a contractor within lease holidays.

.. _EscalationClauses:

EscalationClauses
=================

Schema
------

:id:
    string, auto-generated, read-only

:escalationPeriodicity:
    `Time intervals`_, required

    Periodicity within which the payment will be increasing considering the inflation rate (for example) on a yearly basis.

:escalationStepPercentage:
    decimal, required

    The percentage which indicates the amount of step the monthly payment will be increased/decreased by.

:conditions:
    string, required, multilingual

    The details for the way of monthly payment to be increased/decreased.

**********
References
**********

.. target-notes::

.. _`Time intervals`: https://en.wikipedia.org/wiki/ISO_8601#Time_intervals

.. _`ISO8601 duration`: https://en.wikipedia.org/wiki/ISO_8601#Durations
