===========================
Beter Benutten MMRI project
===========================

This project contains testing code and data for the Beter Benutten MMRI project.

See the `project source`_ at GitHub.

.. _`project source`: https://github.com/plannerstack/mmri


Specification
=============

The test-set is based on the requirements document developed in the Beter Benutten MMRI project. The documents contains an informal set of requirements, which this project attempts to formalize and test.

The formalization of the requirements is written in LaTeX and can be found here: :file:`specs/testset.tex`. Every requirement is tested as a single testcase and is defined as a transit graph, a list of planning requests and the correct results.


Test data
=========

The data sets of the testcases can be found as GTFS here: :file:`data/gtfs`.


Setting up a development environment
====================================

Using Virtualenv_ is recommended. Use the following commands to set-up a
development environment::

    virtualenv .
    . bin/activate
    pip install -r dev_requirements.txt

.. _Virtualenv: http://virtualenv.org


Planner testing
===============

Currently, only testing an OpenTripPlanner_ installation is supported.


Running the static tests
------------------------

The tests are located at :file:`tests/static-tests.json`. Use the
:program:`mmri-test-runner` command to start the tests.

.. program-output:: mmri-test-runner --help

For example::

    mmri-test-runner -p otp -u http://opentripplanner.nl/opentripplanner-api-webapp/ws/plan tests/static-tests.json output.json

.. _OpenTripPlanner: http://www.opentripplanner.org


Data format
-----------

Test input and output use JSON_. Date / time is formatted in `ISO 8601`_ format, but without timezone information.

.. _JSON: http://en.wikipedia.org/wiki/JSON
.. _`ISO 8601`: http://en.wikipedia.org/wiki/ISO_8601


Test input is a JSON array containing objects representing individual testcases. For example:

.. code-block:: json

    [
        {
            "id": 9,
            "from": {
                "latitude": 52.06972,
                "longitude": 4.3225,
                "description": "Station Den Haag HS"
            },
            "to": {
                "latitude": 52.080276,
                "longitude": 4.325,
                "description": "Station Den Haag Centraal"
            },
            "time": "2013-05-13T12:00:00",
            "timeType": "D",
            "comment": "Tram is sometimes faster than train"
        }
    ]

A testcase defines the following properties:

``id``
    A test identifier. Used to match test output.

``from``
    The start location, an object containing ``latitude``, ``longitude`` and ``description`` properties or the ``stopId`` for stop-to-stop planning

``to``
    The destination location, using the the same format as ``from``.

``time``
    The date and time of departure or arrival.

``timeType``
    Whether the ``time`` property is a departure time (``D``) or arrival time (``A``).

``comment``
    Comments describing the test-case.

``preferLeastTransfers``
    Wether having less transfers is preferred

``preferredTravelType``
    The preferred travel type, for instance ``bus``

``bannedRoute``
    The route to ban during a trip, defined by the routeId

``bannedStop``
    The stop to ban during a trip, defined by the StopId

``wheelchairAccessible``
    Whether the trip should be wheelchairAccessible


Test output is a JSON array containing objects representing test results. For example:

.. code-block:: json

    [
        {
          "id": 9,
          "departureTime": "2013-05-13T12:03:00",
          "arrivalTime": "2013-05-13T12:07:00",
          "duration": 240,
          "transfers": 0,
          "legs": [
            {
              "departureTime": "2013-05-13T12:03:00",
              "arrivalTime": "2013-05-13T12:07:00",
              "line": "Intercity (Den Haag Centraal)"
            }
          ]
        }
    ]

A test result defines the following properties:

``id``
    The test identifier. Used to match test input.

``departureTime``
    The date and time of departure (in json datetime format).

``arrivalTime``
    The date and time of arrival (in json datetime format).

``duration``
    The total length of the trip (in seconds).

``transfers``
    The number of transfers.

``departureStopId``
    The id of the departure stop without the agency prefix.

``arrivalStopId``
    The id of the arrival stop without the agency prefix.

``legs``
    A list of trip legs, an object containing ``departureTime``, ``arrivalTime`` and ``line`` properties.
