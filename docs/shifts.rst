Shifts
======

TODO: high level overview of the shift model.


Schema
------

TODO: specification for the shift schema and validation.


Endpoints
---------
.. http:get:: /api/v1/shifts/

   The list view of all shifts.

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
        "next": "http://example.com/api/v1/shifts/?page=2"
        "prev": null,
        "count": 123,
        "results": [
          {
            "id": 1,
            ...
          },
          {
            "id": 2,
            ...
          },
          ...
        ]
      }

   :query integer page: Specify which page of results.
   :query integer page_size: Page size for results.  Max 100.
   :query integer order: Sort the results.  TODO: list choices.
   :query integer shift_length{__lt,__lte,__gt,__gte,__between,__ibetween,__lbetween,__rbetween}: Filter to shifts based on their ``shift_length``
   :query datetime start_time{__lt,__lte,__gt,__gte,__between,__ibetween,__lbetween,__rbetween}: Filter to shifts based on their ``start_time``
   :query integer owner{__ne}: Filter to shifts based on the primary key of its owner.
   :query integer department{__ne}: Filter to shifts based on the primary key of its department.
   :query boolean requires_code: If ``True``, only return shifts which require a code to claim.  If ``False``, only return shifts which do **not** require a code to claim.

   :>json string next: The url of the next page of results. `null` if no next page.
   :>json string prev: The url of the previous page of results. `null` if no next page.
   :>json number count: The total number of records.
   :>json array results: The shift objects.  See the detail view for the individual object schema.

   :statuscode 200: success.
   :statuscode 403: permissions error.


.. http:post /api/v1/shifts/

   Create a new shift entry.

   **Example request**:

   .. sourcecode:: http

      Content-Type: application/json

      {
        ...  # TODO
      }

   **Example error response**:

   .. sourcecode:: http

      HTTP/1.1 400 OK
      Vary: Accept
      Content-Type: application/json

      {
        "owner": ["This field is required"]
      }

   TODO: POST data schema

   :statuscode 201: successful creation.
   :statuscode 400: validation error.  Response body contains error details.
   :statuscode 403: permissions error.

.. http:get:: /api/v1/shifts/:id/

   The detail view for a single shift.

   **Example response**:

   .. sourcecode:: http

      Content-Type: application/json

      {
        "id": 1,
        ...
      }

   :>json number id: The primary key of the shift.
   TODO: the rest of the schema

   :statuscode 200: success.
   :statuscode 404: not found.
   :statuscode 403: permissions error.

.. http:put:: /api/v1/shifts/:id/

   The detail view for a single shift.

   **Example request**

   .. sourcecode:: http

      Content-Type: application/json

      {
        ...  # TODO
      }

   **Example response**

   .. sourcecode:: http

      Content-Type: application/json

      {
        "id": 1,
        ...  # TODO
      }

   :statuscode 200: success.
   :statuscode 404: not found.
   :statuscode 403: permissions error.

   :>json integer department: The primary key of the ``Department`` the shift belongs to.  Required.
   :>json datetime start_time: A datetime in `ECMA 262 date time string specification`_.  (Example ``2013-01-29T12:34:56.123Z``).  All dates are in Mountain Time (``UTC-0700``).
   :>json integer shift_length: Number of hours in the shift.  Must be greater than zero and less than or equal to 24 (``0 < n <= 24``).  Requireds.
   :>json integer owner: The primary key of the ``User`` who has claimed the shift.  Optional.  Nullable.
   :>json string code: Code required to claim shift.  Optional.  If falsy, shift will not required a code.  Nullable.


.. http:patch:: /api/v1/shifts/:id/

    When making a ``PATCH`` request, only the fields that are posted are
    validated.  This is useful for updating a single field, without caring what
    the other values need to be such as claiming a shift.


.. _ECMA 262 date time string specification: http://ecma-international.org/ecma-262/5.1/#sec-15.9.1.15
