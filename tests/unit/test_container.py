# -*- coding: utf-8; -*-
from unittest import mock

import pytest

from dockerfixtures.image import Image
from dockerfixtures.container import Container, _CONTAINER_DEFAULT_OPTIONS


def test_container_image_attribute_is_set():
    # Given
    image = Image('')

    # When
    cntr = Container(image)

    # Then
    assert cntr.image is image


def test_container_environment_inherits_image_environment(dummy_env, client, running_container):
    # given
    image = Image('', environment=dummy_env)
    cntr = Container(image, poll_interval=0)

    # When
    cntr.run(dockerclient=client)

    # Then
    client.containers.run.assert_called_once_with(image=image.pullname,
                                                  environment=dummy_env,
                                                  **cntr.options)


def test_container_options_inherit_default_options():
    # Given
    image = Image('')

    # When
    cntr = Container(image)

    # Then
    assert cntr.options == _CONTAINER_DEFAULT_OPTIONS


def test_container_never_run_has_no_id():
    # Given
    image = Image('')

    # When
    cntr = Container(image)

    # Then
    assert cntr.id is None


def test_container_run_raises_runtime_error_when_exited(client,
                                                        container_exited_after_reload):
    """
    """
    # Given
    image = Image('')
    cntr = Container(image)

    # When
    with pytest.raises(RuntimeError):
        cntr.run(dockerclient=client)

    # Then
    container_exited_after_reload.reload.assert_called_once_with()


def test_container_running(client, container_running_after_reload):
    """
    """
    # Given
    image = Image('')
    cntr = Container(image)

    # When
    result = cntr.run(dockerclient=client)

    # Then
    assert result == container_running_after_reload.id
    container_running_after_reload.reload.assert_called_once_with()


def test_container_running_after_second_reload(client, container_running_after_2_reload):
    """
    """
    # Given
    poll_interval = 10
    image = Image('')
    cntr = Container(image, poll_interval=poll_interval)

    # When
    with mock.patch('dockerfixtures.container.time') as time:
        result = cntr.run(dockerclient=client)

    # Then
    assert container_running_after_2_reload.id == result
    assert container_running_after_2_reload.reload.call_count == 2
    time.sleep.assert_called_once_with(poll_interval)


def test_container_as_a_context_manager(client, running_container):
    # Given
    image = Image('')
    cntr = Container(image, dockerclient=client, max_wait=0)

    # When
    with cntr:
        pass

    assert client.containers.run.called
    assert running_container.kill.called


def test_container_as_a_context_manager_raises_if_no_client():
    # Given
    image = Image('')
    cntr = Container(image)

    # Ensure
    with pytest.raises(ValueError):
        # When
        with cntr:
            pass


def test_container_as_a_context_manager_reraises_exception(client, running_container):
    # Given
    image = Image('')
    cntr = Container(image, dockerclient=client, max_wait=0)

    # Ensure
    with pytest.raises(Exception, match='^1234$'):
        # When
        with cntr:
            raise Exception('1234')


# vim: et:sw=4:syntax=python:ts=4:
