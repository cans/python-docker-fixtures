============================================
Docker containers as test fixtures made easy
============================================

.. image:: https://badge.fury.io/py/dockerfixtures.svg
    :alt: Latest version on Pypi: ?
    :target: https://badge.fury.io/py/dockerfixtures
.. image:: https://img.shields.io/pypi/pyversions/dockerfixtures.svg
    :alt: Supported Python versions: ?
    :target: https://pypi.org/project/dockerfixtures
.. image:: https://travis-ci.com/cans/python-docker-fixtures.svg?branch=master
    :alt: Build status (travis.com): ?
    :target: https://travis-ci.com/cans/python-docker-fixtures
.. image:: https://circleci.com/gh/cans/python-docker-fixtures.svg?style=svg
    :alt: Build status (circleci.com): ?
    :target: https://circleci.com/gh/cans/python-docker-fixtures
.. image:: https://codecov.io/gh/cans/python-docker-fixtures/branch/master/graph/badge.svg
    :alt: Test coverage: ? %
    :target: https://codecov.io/gh/cans/python-docker-fixtures


This package was inspired by others, but after trying to make heads and tails
of them when faced with bugs, I ended-up finding simpler to start over.

Using dockerfixtures with pytest
================================

To spawn a container in your tests, proceed as follow:

.. code-block:: Python

    import docker
    from dockerfixtures import image, container
    import pytest

    @pytest.fixture(scope='session')
    def docker_client():
         return docker.from_env()

    @pytest.fixture(scope='session')
    def pg_image() -> image.Image:
        return image.Image('postgres', tags='12')

    @pytest.fixture(scope='function')
    def pg_container(docker_client: docker.client.DockerClient,
                     pg_image: image.Image) -> container.Container:
        yield from container.fixture(docker_client, some_image)

    # If you don't need to reuse the image

    @pytest.fixture(scope='session')
    def pg_container(docker_client) -> container.Container:
        some_image = image.Image('postgres', tags='12')
        yield from container.fixture(docker_client, some_image)


Why not a pytest plugin ?
=========================

Other implementation of this have been provinding a pytest
plugin, so you might wonder why this one doesn't ?

First reason is I have not looked into it that much, yet.

But anyhow, you would still need to import the
``dockerfixtures.image`` module. So I am not very sure what the
benefits would be ?

Also I found those plugins to provide somewhat bizarre API, for
example to define the fixtures' scope. I haven't looked into
why they do that, yet. Here there are no surprises, a container
fixture looks like any other fixture.

Pytest plugins are global: they have to be imported in your
`top-level`_ ``conftest.py`` (see note). I think it is good
practice to keep your tests properly partitioned based on their
external dependencies. It can help split workload if the need
arises. In a collaborative environment, having to import
``dockerfixtures``, may help prevent breaking that partitioning
during reviews.


.. _top-level: https://docs.pytest.org/en/latest/writing_plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file
