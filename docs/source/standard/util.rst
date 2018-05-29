.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Period, startDate, endDate
.. _Period:

Period
======

Schema
------

:startDate:
    string, :ref:`Date`

    |ocdsDescription|
    The start date for the period.

:endDate:
    string, :ref:`Date`

    |ocdsDescription|
    The end date for the period.

`startDate` should always precede `endDate`.

.. _Date:

Date
====

Date/time in :ref:`date-format`.

.. index:: Value, Currency, VAT
.. _Value:

Value
=====

Schema
------

:amount:
    float, required

    |ocdsDescription|
    Amount as a number.

    Should be positive.

:currency:
    string, required

    |ocdsDescription|
    The currency in 3-letter ISO 4217 format.

:valueAddedTaxIncluded:
    bool, required

.. index:: Revision, Change Tracking
.. _revision:

Revision
========

Schema
------

:date:
    string, :ref:`Date`

    Date when changes were recorded.

:changes:
    List of `Change` objects


.. _Guarantee:

Guarantee
=========

Schema
------

:amount:
    float, required

    |ocdsDescription|
    Amount as a number.

    Should be positive.

:currency:
    string, required, default = `UAH`

    |ocdsDescription|
    The currency in 3-letter ISO 4217 format.

