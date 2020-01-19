# -*- coding: utf-8; -*-
from dockerfixtures.container import Container
from dockerfixtures.image import Image


def test_container_ports_when_image_already_available(mocker, client, running_container):
    # Given
    cntr = Container(Image(''), dockerclient=client)
    cntr.run()

    # When
    ports = cntr.ports

    # Then
    assert ports == {'1234/tcp': (1234, 'tcp'), }


def test_container_ports_when_image_not_available(mocker,
                                                  client,
                                                  container,
                                                  image_metadata,
                                                  docker_image,
                                                  ):
    # Given
    get_registry_data = mocker.patch.object(client.images,
                                            'get_registry_data',
                                            return_value=image_metadata)
    image = Image('')
    cntr = Container(image, dockerclient=client)

    # When
    ports = cntr.ports

    # Then
    assert ports == {'1234/tcp': (1234, 'tcp'), }
    get_registry_data.assert_called_once_with(name=image.pullname)


# vim: et:sw=4:syntax=python:ts=4:
