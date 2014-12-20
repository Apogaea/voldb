API Documentation
=================

Notation
--------

Query Parameters
~~~~~~~~~~~~~~~~

Validation
..........

Query parameters which do not pass validation will be silently ignored.

Truthyness and Falsyness
........................

For query parameters which expect a boolean, the following values are interpreted as ``True``.

* the string ``'true'``
* the string ``'True'``
* the number ``1``

For query parameters which expect a boolean, the following values are interpreted as ``False``.

* the string ``'false'``
* the string ``'False'``
* the number ``0``
* the value ``null``

Comparison notation
...................

  For query parameters which need comparisons beyond equality or truthyness,
  the following notation is used.

  :query_param integer size{__lt,__gt}: 

  In this example, the ``size`` query parameter can be sent in three formats.

  * ``/endpoint/?size=3``

    All results with size equal to 3

  * ``/endpoint/?size__lt=3``

    All results with size less than 3

  * ``/endpoint/?size__gt=3``

    All results with size greater than 3

  The following suffixes map to the followin comparisons.

  * ``__lt: <``
  * ``__lt=: <=``
  * ``__gt: >``
  * ``__gte: >=``
  * ``__ne: !=``
  * ``__between l < x < r`` *(non-inclusive of endpoints)*
  * ``__ibetween l <= x <= r`` *(inclusive of endpoints)*
  * ``__lbetween l <= x < r`` *(left inclusive of endpoints)*
  * ``__rbetween l < x <= r`` *(right inclusive of endpoints)*

  For ``between`` comparisons, the two values should be separated by a comma.

  * ``/endpoint/?size__between=1,8``

    All sizes between 1 and 8,
