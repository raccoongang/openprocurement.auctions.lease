.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Contract, ContractTerms, LeaseTerms, TaxHolidays, EscalationClauses
.. _Contract:

Contract
========

Schema
------

:id:
    UID, auto-generated

    |ocdsDescription|
    The identifier for this contract.

:awardID:
    string, required

    |ocdsDescription|
    The ``Award.id`` against which this contract is being issued.

:contractID:
       string, auto-generated, read-only

:contractNumber:
       string

:title:
    string, required

    |ocdsDescription|
    Contract title

:description:
    string

    |ocdsDescription|
    Contract description

:value:
    :ref:`Value` object, auto-generated, read-only

    |ocdsDescription|
    The total value of this contract.

:items:
    List of :ref:`Item` objects, auto-generated, read-only

    |ocdsDescription|
    The goods, services, and any intangible outcomes in this contract. Note: If the items are the same as the award, do not repeat.

:suppliers:
    List of :ref:`Organization` objects, auto-generated, read-only

:status:
    string, required

    |ocdsDescription|
    The current status of the contract.

    Possible values are:

    * `pending` - this contract has been proposed, but is not yet in force.
      It may be awaiting signature.
    * `active` - this contract has been signed by all the parties, and is
      now legally in force.
    * `cancelled` - this contract has been cancelled prior to being signed.
    * `terminated` - this contract was signed and in force, and has now come
      to a close.  This may be due to a successful completion of the contract,
      or may be early termination due to some non-completion issue.

:period:
    :ref:`Period`

    |ocdsDescription|
    The start and end date for the contract.

:dateSigned:
    string, :ref:`Date`

    |ocdsDescription|
    The date the contract was signed. In the case of multiple signatures, the date of the last signature.

:date:
    string, :ref:`Date`

    The date when the contract was changed or activated.

:documents:
    List of :ref:`Document` objects

    |ocdsDescription|
    All documents and attachments related to the contract, including any notices.

.. _ContractTerms:

ContractTerms
=============

Schema
------

:contractType:
    string, required

    The only value for this field is ``lease``.

:leaseTerms:
    :ref:`LeaseTerms`

    The options of property lease.

.. _LeaseTerms:

LeaseTerms
==========

Schema
------

:leaseDuration:
    ISO8601 duration object, required

    Property lease duration in contract.

:taxHolidays:
    list of :ref:`TaxHolidays`

    A period during which a person or company is allowed to pay no payment or less than usual.

:escalationClauses:
    list of :ref:`EscalationClauses`

.. _TaxHolidays:

TaxHolidays
===========

Schema
------

:taxHolidaysDuration:
    ISO8601 duration object, required

    Duration of rent holidays.

:conditions:
    string, required, multilingual

    Lease rent holidays conditions in Ukrainian.

:value:
    :ref:`Value` object, required

    The lease value for tax holidays.

.. _EscalationClauses:

EscalationClauses
=================

Schema
------

:id:
    string, auto-generated, read-only

:escalationPeriodicity:
    Time intervals, required

    Periodicity of escalation.

:escalationStepPercentageRange:
    decimal, required

    Percentage range for escalation.

:conditions:
    string, required, multilingual

    Lease rent escalation conditions in Ukrainian.
