# -*- coding: utf-8; -*-
from dockerfixtures.image import Image
from dockerfixtures.container import Container


def test_container_address_when_no_network_settings(client, container_lacking_network_settings):
    # Given
    cntr = Container(Image(''), dockerclient=client)
    cntr.run()

    # When
    address = cntr.address

    # Then
    assert address == 'localhost'


# vim: et:sw=4:syntax=python:ts=4:
