============
Installation
============


Setting up a development environment
====================================

Using Virtualenv_ is recommended. Use the following commands to set-up a
development environment:

.. code-block:: console

    $ virtualenv .
    $ . bin/activate
    $ pip install -r dev_requirements.txt

Activating the `virtualenv` should be done every time before working on the
code or running the tests.

.. _Virtualenv: http://virtualenv.org


Building and installing the package
===================================

From the development environment you can build a source package:

.. code-block:: console

    python setup.py sdist

The package can be found in :file:`dist/mmri-VERSION.tar.gz`. You can copy it
to the machine you want to run the tests on and install it by executing:

.. code-block:: console

    pip install PACKAGE
