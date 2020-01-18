============================================
Docker containers as test fixtures made easy
============================================

.. image:: https://travis-ci.com/cans/python-docker-fixtures.svg?branch=master
    :target: https://travis-ci.com/cans/python-docker-fixtures
.. image:: https://circleci.com/gh/cans/python-docker-fixtures.svg?style=svg
    :target: https://circleci.com/gh/cans/python-docker-fixtures
.. image:: https://codecov.io/gh/cans/python-docker-fixtures/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/cans/python-docker-fixtures


This package was inspired by others, but was written from
scratch. But after trying to make heads and tails of them
when faced with bugs, I ended-up finding simpler to start
over.

Using dockerfixtures with pytest
================================

To spawn a container in your tests, proceed as follow:


.. code:: Python

    from dockerfixtures import Image, Container
    import pytest


    @pytest.fixture(scope='session')
    def some_image():
        return image.Image('postgres', tags='12')
       
    @pytest.fixture(scope='session')
    def some_container_fixture(some_image):
        yield from container.fixture(some_image)
