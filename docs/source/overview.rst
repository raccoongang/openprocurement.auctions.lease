Overview
========

This ``openprocurement.auctions.lease`` package documentation contains information for Users
of the PROZORRO.SALE system and intends to discover all aspects of ``lease procedure``.


The following subjects can act as an Organizer:

* `State Property Fund of Ukraine`_;

* state-owned enterprises;

* the authorities, that are authorized by the Supreme Council of the Autonomous Republic of Crimea;

* enterprises, institutions and organizations.


To perform state property lease specialized procedure is available:

 * ``propertyLease`` - lease of the state property.

Features
--------

* The only date Organizer has to provide is ``Auction.auctionPeriod.startDate`` - approximate date when the auction starts - the actual value will be calculated automatically considering the existing capacity.

* The rest dates and periods will be calculated automatically based on ``Auction.auctionPeriod.startDate``.

* Optionally an Organizer can set ``rectificationPeriod.endDate``, if not provided - it will be calculated automatically.

* ``tenderPeriod`` duration must be at least 7 calendar days.

* Optionally an Organizer can set ``tenderPeriod.endDate`` - if so, auction can't start earlier 3 days after.

* An Organizer can edit the procedure only during ``rectificationPeriod`` (e.g. increase and decrease ``value.amount``, ``guarantee.amount``, ``minimalStep.amount``).

* Organizer can add and edit documents only during ``rectificationPeriod``.

* As soon as the procedure is edited, the status of all of the submitted bids will be switched to ``invalid``.

* Procedure can be switched from ``draft`` status to ``active.tendering``.

* During ``enquiryPeripod`` participants can ask questions, submit proposals, and upload documents.

* All of the identifiers within the scheme ``CPVS`` can be chosen. ``PA01-7`` is the one to be added automatically.

* The minimum desired participants' number by default is 2, but there is option to decrease it explicitly to 1 participant;

* The only currency (``value.currency``) for this procedure is hryvnia (UAH).

* The items within an procedure are allowed to be from different CAV-PS groups.

.. note:: There is predefined list of possible items to lease.

* There is obligatory participant qualification via guarantee payment.

* The only criterion for choosing a winner is the price, provided the bidder complies with the qualifying criteria determined by the Organizer.

Conventions
-----------

API accepts `JSON`_ or form-encoded content in
requests.  It returns JSON content in all of its responses, including
errors.  Only the UTF-8 character encoding is supported for both requests
and responses.

All API POST and PUT requests expect a top-level object with a single
element in it named ``data``.  Successful responses will mirror this format.
The data element should itself be an object, containing the parameters for
the request.  In the case of creating a new auction, these are the fields we
want to set on the auction itself.

If the request was successful, we will get a response code of ``201``
indicating the object was created.  That response will have a data field at
its top level, which will contain complete information on the new auction,
including its ID.

If something went wrong during the request, we'll get a different status
code and the JSON returned will have an ``errors`` field at the top level
containing a list of problems.  We look at the first one and print out its
message.

Project status
--------------

The project currently is in `beta` status.

The source repository for this project is on GitHub:
https://github.com/openprocurement/openprocurement.auctions.lease

You can leave feedback by raising a new issue on the `Issue tracker
<https://github.com/openprocurement/openprocurement.auctions.lease/issues>`_ (GitHub
registration necessary).

Documentation of related packages
---------------------------------

* `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_

API stability
-------------

API is relatively stable.


Change log
----------
1.1.1-sale


0.1.0

Released: not released

Next steps
----------
You might find it helpful to look at the :ref:`tutorial`.

**********
References
**********

.. target-notes::

.. _`State Property Fund of Ukraine`: http://www.spfu.gov.ua
.. _`JSON`: http://json.org/
