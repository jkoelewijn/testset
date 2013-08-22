===============
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
