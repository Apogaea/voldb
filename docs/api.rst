API Documentation
=================

Shifts
------

TODO: high level overview of the shift model.


Schema
~~~~~~

TODO: specification for the shift schema and validation.


Endpoints
~~~~~~~~~
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

   :query page: Integer for the desired page of results.
   :query page_size: Integer for the page size for results.  Max 100.

   :>json string next: The url of the next page of results. `null` if no next page.
   :>json string prev: The url of the previous page of results. `null` if no next page.
   :>json number count: The total number of records.
   :>json object results: The shift objects.  See the detail view for the individual object schema.

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


.. http:put /api/v1/shifts/:id/
   http:patch /api/v1/shifts/:id/

   The detail view for a single shift.

   **Example request**

   .. sourcecode:: http

      Content-Type: application/json

      {
        "id": 1,
        ...
      }

   TODO: PUT/PATCH parameters.

   :statuscode 200: success.
   :statuscode 404: not found.
   :statuscode 403: permissions error.
