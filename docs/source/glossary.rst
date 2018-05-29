Glossary
========

Tender Procedure
    a process which includes:

    * lease tender procedure initialization by an Organizer;

    * initial bids proposals by Participants (Bidders);

    * auction (3 rounds);

    * qualification (awarding) - identifying of the winner;

    * payment;

    * contract signing;

Organizer
    lease procedure initiator

Minimum number of qualified bids [``minNumberOfQualifiedBids``]
    minimum desired participants' count to consider procedure successful


Invalidation date [``invalidationDate``]
    date when the last editing was made by an Organizer (initial bids invalidation occurs)

Valid bid
    a bid which value is equal or greater then a value of ``value.amount + minimalStep``

CAV-PS
    the main classifier

CPVS (Common Procurement Vocabulary)
    additional (secondary) classifier

Tender Procedure life cycle
    consists of the following periods:

    * ``tenderPeriod`` - the time period during which tender ``bids`` are accepting;

    * ``enquiryPeriod`` - the time period during which participants can ask ``questions`` to clarify tender's terms;

    * ``rectificationPeriod`` - the time period during which an Organizer can perform changes to tender terms;

    * ``auctionPeriod`` - the time period of ``auction`` itself;

    * ``verificationPeriod`` - the time period during which an Organizer identifies a winner;

    * ``paymentPeriod`` - the time period during which Participant (Winner) performs payment;

    * ``signingPeriod`` - the time period of downloading and activating of Contract by an Organizer;

.. image:: images/auction_lifecycle.png

.. note::

    * ``tenderPeriod`` has to be at least 5 days longer than ``rectificationPeriod``;
    * as a result of verification process is auction ``Protocol`` (confirmed and downloaded by an Organizer);
    * every period has its ``startDate`` and ``endDate``.
