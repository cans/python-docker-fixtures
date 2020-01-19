# -*- coding: utf-8; -*-
import docker.errors
import pytest

from dockerfixtures.container import Container, ImageNotFound, TimeOut
from dockerfixtures.image import Image


def test_container_paused_then_running(mocker, client, container_paused_after_1st_reload):
    """
    """
    # Given
    poll_interval = 10.0
    image = Image('')
    cntr = Container(image, max_wait=2, startup_poll_interval=poll_interval)
    sleep = mocker.patch('dockerfixtures.container.time.sleep')

    # When
    result = cntr.run(dockerclient=client)

    # Then
    # call count is 2 because reload is call one last time before raising
    assert container_paused_after_1st_reload.id == result
    assert container_paused_after_1st_reload.reload.call_count == 2
    sleep.assert_called_once_with(poll_interval)


def test_container_run_raises_runtime_error_when_exited(client,
                                                        container_exited_after_reload):
    """
    """
    # Given
    image = Image('')
    cntr = Container(image)

    # Ensure
    with pytest.raises(RuntimeError):
        # When
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


def test_container_running_after_second_reload(mocker, client, container_running_after_2_reload):
    """
    """
    # Given
    poll_interval = 10.0
    image = Image('')
    cntr = Container(image, startup_poll_interval=poll_interval)
    sleep = mocker.patch('dockerfixtures.container.time.sleep')

    # When
    result = cntr.run(dockerclient=client)

    # Then
    assert container_running_after_2_reload.id == result
    assert container_running_after_2_reload.reload.call_count == 2
    sleep.assert_called_once_with(poll_interval)


def test_container_run_raises_image_not_found_when_registry_says_so(mocker, client):
    # Given
    image = Image('')
    mocker.patch.object(client.images, 'pull', side_effect=docker.errors.ImageNotFound(''))

    # Ensure
    with pytest.raises(ImageNotFound):
        # When
        Container(image).run(dockerclient=client)


def test_container_run_raises_runtime_warning_when_unkwown_status(client,
                                                                  container_unknown_on_1st_reload):
    """
    """
    # Given
    image = Image('')
    cntr = Container(image, startup_poll_interval=0.0)

    # Ensure
    with pytest.warns(RuntimeWarning):
        # When
        cntr.run(dockerclient=client)

    # Then
    assert container_unknown_on_1st_reload.reload.call_count == 2


def test_container_run_times_out(mocker, client, container):
    # Given
    cntr = Container(Image(''),
                     dockerclient=client,
                     max_wait=0.000000001,
                     startup_poll_interval=0.0)
    mocker.patch('dockerfixtures.container.time.sleep')  # bypass time.sleep()

    # Ensure
    with pytest.raises(TimeOut):
        # When
        cntr.run()

    # Then
    assert container.reload.call_count == 0

# vim: et:sw=4:syntax=python:ts=4:
