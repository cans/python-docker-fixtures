# -*- coding: utf-8; -*-
import pytest

from dockerfixtures.container import Container
from dockerfixtures.image import Image


def test_container_address_when_no_network_settings(client, container_lacking_network_settings):
    # Given
    cntr = Container(Image(''), dockerclient=client)
    cntr.run()

    # When
    address = cntr.address

    # Then
    assert address == 'localhost'


def test_container_address_raises_runtime_error_when_not_started():
    # Given
    cntr = Container(Image(''))

    # Ensure
    with pytest.raises(RuntimeError):
        # When
        cntr.address


# vim: et:sw=4:syntax=python:ts=4:
