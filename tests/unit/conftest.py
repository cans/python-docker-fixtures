# -*- coding: utf-8; -*-
import os
from unittest import mock

import pytest

from dockerfixtures import container as c
from dockerfixtures.ci import CONTAINERIZED_CI_VENDOR_VARS


@pytest.fixture(params=(
    pytest.param((('CI', 'CIRCLECI', None), True, ), id='within circleci container'),
    pytest.param((('CI', 'CIRCLECI', 'VIRTUAL_MACHINE'), False, ), id='within circleci machine'),
    pytest.param((('CI', 'GITHUB_ACTION', None), True, ), id='within github action'),
    pytest.param(((None, 'GITHUB_ACTION', None), False, ), id='ignores other vars if CI undefined'),
    pytest.param((('CI', None, None), False), id='within non-dockerized CI'),
    pytest.param((('CI', None, 'VIRTUAL_MACINE'), False),
                 id='within non-dockerized CI (VM defined)'),
))
def ci_environment(request, monkeypatch):
    variables_to_unset = {0: ['CI'],
                          1: CONTAINERIZED_CI_VENDOR_VARS,
                          2: ['VIRTUAL_MACHINE'],
                          }
    variables, expected = request.param
    for idx, var in enumerate(variables):
        if var is not None:
            monkeypatch.setenv(var, '<value does not matter>')
            continue
        # 'cause these tests may run in a CI where these variables may be defined
        for variable in [v for v in variables_to_unset[idx] if v in os.environ]:
            monkeypatch.delenv(variable)
    return expected


@pytest.fixture
def client(container, docker_image):
    """A mock :class:`~docker.client.DockerClient`

    Has the following methods mocked:
    - :meth:`~docker.client.DockerClient.containers.run`.

    """
    mock_client = mock.Mock()
    mock_client.images.pull = mock.Mock(return_value=docker_image)
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
def container_w_command(running_container):
    """A docker container object mock-up (as produced by the docker library)
    """
    running_container.image.attrs.pop('Config')

    return running_container


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
    image.attrs = {'ExposedPorts': {'1234/tcp': {}},
                   'Config': {'Entrypoint': ['abc'], }, }
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
