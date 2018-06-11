.. include:: defs.hrst

.. index:: Item, PropertyLeaseClassification, CAV, CPV, Unit

.. _Item:

Item
====

Schema
------

:id:
    string, required, auto-generated

:description:
    string, multilingual, required

    A description of the property to be leased.

    Auction subject / asset description.

:classification:
    :ref:`PropertyLeaseClassification`, required

    |ocdsDescription|
    The primary classification for the item. See the `itemClassificationScheme` to
    identify preferred classification lists.

    The only primary classifier is CAV-PS.
    Additionally, there is a validation for the input of this classifier due to which
    the accuracy of at least a class has to be used.

:additionalClassifications:

    List of :ref:`Classification` objects

    Additional classifier is CPVS. The property can be leased, when entering value PA01-7
    in the classifier CPVS field.

    |ocdsDescription|
    An array of additional classifications for the item.
    See the `itemClassificationScheme` codelist for common options to use in OCDS.

:address:
    :ref:`Address`

    Address, where the item is located.
    Classification codes (CAV-PS) for which ``item.address`` object is optional are given below:

    :download:`CPV <../tutorial/cpv_codes_item_address_optional.json>`

    :download:`CAV_v2 <../tutorial/cav_v2_codes_item_address_optional.json>`


:location:
    dictionary

    Geographical coordinates of the location. Element consists of the following items:

    :latitude:
        string, required
    :longitude:
        string, required
    :elevation:
        string, optional, usually not used

    `location` usually takes precedence over `address` if both are present.

:contractPeriod:
     :ref:`Period`

     The period which is used to indicate the duration of a contract within which it is valid.
     Contract period represents the start and end date for the contract signed after the property or asset has been sold.
     It is also can be used to specify the timeframe of a contact for a lease.

:unit:
    :ref:`Unit`

    |ocdsDescription|
    Description of the unit which the good comes in e.g.  hours, kilograms.
    Made up of a unit name, and the value of a single unit.

:quantity:
    decimal

    |ocdsDescription|
    The number of units required.

.. :relatedLot:
    string

    ID of related :ref:`Lot`.


.. _Classification:

Classification
==============

Schema
------

:scheme:
    string, required

    |ocdsDescription|
    A classification should be drawn from an existing scheme or list of
    codes. This field is used to indicate the scheme/codelist from which
    the classification is drawn. For line item classifications, this value
    should represent a known Item Classification Scheme wherever possible.

:id:
    string, required

    |ocdsDescription|
    The classification code drawn from the selected scheme.

:description:
    string, required, multilingual

    |ocdsDescription|
    A textual description or title for the code.

:uri:
    uri

    |ocdsDescription|
    A URI to identify the code. In the event individual URIs are not
    available for items in the identifier scheme this value should be left
    blank.

.. _Unit:

Unit
====

Schema
------

:name:
    string

    |ocdsDescription|
    Name of the unit

:code:
    string, required

    UN/CEFACT Recommendation 20 unit code.
