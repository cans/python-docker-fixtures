# -*- coding: utf-8; -*-
from unittest import mock

import pytest

from dockerfixtures import container as c


@pytest.fixture
def client(container):
    """A mock :class:`~docker.client.DockerClient`

    Has the following methods mocked:
    - :meth:`~docker.client.DockerClient.containers.run`.

    """
    mock_client = mock.Mock()
    mock_client.containers.run = mock.Mock(return_value=container)

    return mock_client


@pytest.fixture
def container():
    """A docker container object mock-up (as produced by the docker library)
    """
    def reload():
        """NOOP reload (does not change the container state)
        """
        return

    container_ = mock.Mock()
    container_.id = '0123456789abcdef'
    container_.reload = mock.Mock(side_effect=reload)
    container_.status = 'created'

    return container_


@pytest.fixture
def container_exited_after_reload(container):
    def reload():
        container.status = c.CONTAINER_STATUS_EXITED
        return

    container.reload = mock.Mock(side_effect=reload)

    return container


@pytest.fixture
def container_paused_after_1st_reload(container):
    def reload():
        nonlocal called
        if called:
            container.status = c.CONTAINER_STATUS_RUNNING
        else:
            container.status = c.CONTAINER_STATUS_PAUSED
        called = True
        return

    called = False
    container.reload = mock.Mock(side_effect=reload)
    return container


@pytest.fixture
def container_running_after_reload(container):
    def reload():
        container.status = c.CONTAINER_STATUS_RUNNING
        return

    container.reload = mock.Mock(side_effect=reload)
    return container


@pytest.fixture
def container_running_after_2_reload(container):
    def reload():
        nonlocal called
        if called:
            container.status = c.CONTAINER_STATUS_RUNNING
        called = True
        return

    called = False
    container.reload = mock.Mock(side_effect=reload)
    return container


@pytest.fixture
def container_unknown_on_1st_reload(container):
    def reload():
        nonlocal called
        if called:
            container.status = c.CONTAINER_STATUS_RUNNING
        else:
            container.status = 'whatever'
        called = True
        return

    called = False
    container.reload = mock.Mock(side_effect=reload)
    return container


@pytest.fixture
def dummy_env():
    return {'VAR1': 'VAL1', 'VAR2': 'VAL2'}


@pytest.fixture
def image_metadata(docker_image):
    metadata = mock.Mock()
    metadata.attrs = {'Descriptor': {'mediaType': c.MANIFEST_V2, }, }
    metadata.pull = mock.Mock(return_value=docker_image)
    return metadata


@pytest.fixture
def docker_image():
    image = mock.Mock()
    image.attrs = {'ExposedPorts': {'1234/tcp': {}}, }
    return image


@pytest.fixture
def running_container(container, docker_image):
    """A docker container object mock-up (as produced by the docker library)
    """
    container.status = 'running'
    # Follows Docker API data format
    container.image = docker_image

    return container


@pytest.fixture
def container_lacking_network_settings(container):
    """A docker container object mock-up (as produced by the docker library)
    """
    container.status = 'running'
    # Follows Docker API data format
    container.attrs = {}

    return container


# vim: et:sw=4:syntax=python:ts=4:
