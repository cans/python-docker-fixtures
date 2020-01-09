# -*- coding: utf-8; -*-
import pytest

from dockerfixtures.image import Image
from dockerfixtures.container import _CONTAINER_DEFAULT_OPTIONS, Container


def test_container_image_attribute_is_set():
    # Given
    image = Image('')

    # When
    cntr = Container(image)

    # Then
    assert cntr.image is image


def test_container_environment_inherits_image_environment(dummy_env, client, running_container):
    # Given
    image = Image('', environment=dummy_env)
    cntr = Container(image, startup_poll_interval=0.0)

    # When
    cntr.run(dockerclient=client)

    # Then
    client.containers.run.assert_called_once_with(command=None,
                                                  environment=dummy_env,
                                                  image=client.images.get(image.pullname),
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


@pytest.mark.filterwarnings('ignore:dockerfixtures.container::RuntimeWarning')
def test_container_as_a_context_manager(client, running_container):
    # Given
    image = Image('')

    # When
    with Container(image, dockerclient=client, max_wait=0):
        pass

    assert client.containers.run.called
    assert running_container.kill.called


@pytest.mark.filterwarnings('ignore:dockerfixtures.container::RuntimeWarning')
def test_container_as_a_context_manager_raises_if_no_client():
    # Given
    image = Image('')

    # Ensure
    with pytest.raises(ValueError):
        # When
        with Container(image):
            pass


@pytest.mark.filterwarnings('ignore:dockerfixtures.container::RuntimeWarning')
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
