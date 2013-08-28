========
Planners
========


The test running is designed to be easily extended for other planners.


Supported planners
==================

Currently we support OpenTripPlanner. Support for the HP trip planner is in
development.


Writing a planner module
========================

Create a new Python module in the :py:mod:`mmri` package by copying
:file:`mmri/test_skel.py` to :file:`test_KEY.py`. ``KEY`` will be used as the
provider key on the command line. Add ``KEY`` to the ``PROVIDER_CHOICES``
constant in :file:`mmri/test_runner.py`.

You need to implement the :py:meth:`TestClass.plan_trip` method.

.. py:method:: TestClass.plan_trip(test)

   Plan a trip for a test case and return the result.

   :param test: a dictionary specifying the request parameters
   :rtype: test case result

A test case is a dictionary of the following form:

.. code-block:: python

    {
        'id': '3b1',
        'agencyId': 'MMRI',
        'from': '3b1',
        'to': '3b2',
        'time': '2014-01-01T00:01:00',
        'timeType': 'D',
        'comment': 'depart at 00:01 from Stop 1 heading Stop 2.'
    }

The following properties can be set:

:from:
    The stop id of the departure location.

:to:
    The stop id of the arrival location.

:startTransitTripId:
    A `trip_id` that serves as the start of the trip. Mutually exclusive with
    the `from` property.

:time:
    The requested departure or arrival time.

:timeType:
    Whether the `time` property is a departure time (:const:`'D'`) or an
    arrival time (:const:`'A'`).

:agencyId:
    The `agency_id` that is used in the GTFS data.

:bannedRoute:
    A `route_id` of a route that should not be used during planning.

:bannedStop:
    A `stop_id` of a stop that should not be used during planning.

:preferLeastTransfers:
    A boolean that indicates that the user prefers the trip with the fewest
    number of transfers.

:preferredTravelType:
    The preferred transportation mode. Trips using this mode should be given
    preference.

:wheelchairAccessible:
    A boolean that indicates that the trip must be accessible by wheelchair.

:comment:
    A comment that describes the test case.

A test case result is a dictionary of the following form:

.. code-block:: python

    {
        'id': '3b1',
        'legs': [
            {
                'departureTime': '2014-01-01T00:10:00',
                'arrivalTime': '2014-01-01T00:11:00',
                'departureStopId': '3b1',
                'arrivalStopId': '3b2'
            }
        ]
    }

If the planning fails for some reason, return :py:const:`None` instead.
