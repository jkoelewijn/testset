===============
Planner testing
===============


Before running the tests, the test data must be loaded into the planner. The :file:`tests/*/gtfs` directories contain the GTFS feeds specific for each test. These feeds can be merged using the :program:`merge-gtfs` command:

.. program-output:: merge-gtfs --help

Example:

.. code-block:: console

    $ merge-gtfs tests/*/gtfs merged


Merging the GTFS data
=====================




Running the tests
=================

The tests are located at :file:`tests/tests.json`. Use the :program:`mmri-
test-runner` command to start the tests.

.. program-output:: mmri-test-runner --help

For example::

    mmri-test-runner -p otp -u http://opentripplanner.nl/opentripplanner-api-webapp/ws/plan tests/requests.json tests/expected-responses output.json timings.out

.. _OpenTripPlanner: http://www.opentripplanner.org
