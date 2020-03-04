Django Sample Project
===============================

Sample django project with docker and other bare minimum setup

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

Requirements
------------

* Django 2.2
* Python 3.7

Installation
------------
#. Clone the git repository
#. Build the docker image

      $ docker-compose build
#. Uplift the docker system to create containers

      $ docker-compose up

Basic Commands
--------------

Migrate the database
^^^^^^^^^^^^^^^^^^^^
Migrate database with the following command
::

  $ docker-compose run --rm django python manage.py migrate

Load seed data
^^^^^^^^^^^^^^
Load bare minimum system data with the following command
::

  $ docker-compose run --rm django python manage.py seed

Create superuser account
^^^^^^^^^^^^^^^^^^^^^^^^
::

    $ docker-compose run --rm django python manage.py createsuperuser

Load the fixtures
^^^^^^^^^^^^^^^^^
::

  $ docker-compose run --rm django python manage.py loaddata users.json


Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

