Glossary
========

Tender Procedure
    a process which includes:

    * lease tender procedure conducted by an Organizer;

    * initial bids proposals by Participants (Bidders);

    * auction (3 rounds);

    * qualification (awarding) - identifying of the winner;

    * payment;

    * contract signing;

Organizer
    lease procedure initiator

Minimum number of qualified bids [``minNumberOfQualifiedBids``]
    minimum eligible participant number count to consider procedure successful


Invalidation date [``invalidationDate``]
    date when the last editing was made by an Organizer (initial bids invalidation occurs)

Valid bid
    a bid whose value is equal to or higher than the value of ``value.amount + minimalStep``

CAV-PS & CPV
    the main classifier

CPVS (Common Procurement Vocabulary)
    additional (secondary) classifier

Tender Procedure life cycle
    consists of the following periods:

    * ``tenderPeriod`` - the time span during which tender ``bids`` are being accepted;

    * ``enquiryPeriod`` - the time span during which participants can ask ``questions`` to clarify the tender terms;

    * ``rectificationPeriod`` - the time span during which an Organizer can introduce changes to tender terms;

    * ``auctionPeriod`` - the time span of ``auction`` itself;

    * ``verificationPeriod`` - the time span during which an Organizer identifies a winner;

    * ``paymentPeriod`` - the time span during which the Participant (Winner) makes payment;

    * ``signingPeriod`` - the time span of the contract uploading and activating;

.. image:: images/auction_lifecycle.png

.. note::

    * ``tenderPeriod`` has to be at least 5 days longer than ``rectificationPeriod``;
    * as the result of verification process is auction ``Protocol`` (confirmed and uploaded by an Organizer);
    * every period has its ``startDate`` and ``endDate``.
