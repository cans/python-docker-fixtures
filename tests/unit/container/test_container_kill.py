# -*- coding: utf-8; -*-
import pytest
from requests import exceptions

from dockerfixtures.image import Image
from dockerfixtures.container import Container


def test_container_kill_raises_when_response_is_404(mocker, client, running_container):
    # Given
    response = mocker.Mock()
    response.status_code = 404
    running_container.kill = mocker.Mock(side_effect=exceptions.HTTPError('', response=response))
    cntr = Container(Image(''), dockerclient=client)
    cntr.run()

    # Ensure
    with pytest.raises(exceptions.HTTPError):
        # When
        cntr.kill()


def test_container_kill_catches_when_response_is_409(mocker, client, running_container):
    # Given
    response = mocker.Mock()
    response.status_code = 409
    running_container.kill = mocker.Mock(side_effect=exceptions.HTTPError('', response=response))
    cntr = Container(Image(''), dockerclient=client)
    cntr.run()

    # When
    cntr.kill()


# vim: et:sw=4:syntax=python:ts=4:
