# -*- coding: utf-8; -*-
import builtins
from unittest import mock

import pytest

from dockerfixtures.image import Image
from dockerfixtures.container import Container, TimeOut


def test_container_wait_when_service_does_not_start_fast_enough(mocker):
    # Given
    # Requirement: time_mock.side_effect[-1] - time_mock.side_effect[0] > max_wait
    cntr = Container(Image('unknown', max_wait=5.0))
    mocker.patch('dockerfixtures.container.Container.address',
                 new_callable=mock.PropertyMock,
                 return_value='localhost')
    time_mock = mocker.patch('dockerfixtures.container.time.time',
                             side_effect=[0.1, 0.2, 10.0, 10.0])
    mocker.patch('dockerfixtures.container.socket.socket',
                 side_effect=builtins.ConnectionError())

    # Ensure
    with pytest.raises(TimeOut):
        # When
        cntr.wait((1234, 'tcp'))

    assert time_mock.call_count == 4


def test_container_wait_when_service_starts_fast_enough(mocker):
    # Given
    mocker.patch('dockerfixtures.container.socket.socket')
    mocker.patch('dockerfixtures.container.Container.address',
                 new_callable=mocker.PropertyMock,
                 return_value='localhost')
    cntr = Container(Image('unknown', max_wait=10.0))

    # When
    res = cntr.wait((1234, 'tcp'))

    # Then
    assert res


def test_container_wait_when_service_starts_fast_enough_but_no_port(mocker):
    # Given
    # Requirement: time_mock.side_effect[-1] - time_mock.side_effect[0] > max_wait
    mocker.patch('dockerfixtures.container.socket.socket')
    mocker.patch('dockerfixtures.container.Container.address',
                 new_callable=mock.PropertyMock,
                 return_value='localhost')
    mocker.patch('dockerfixtures.container.Container.ports',
                 new_callable=mock.PropertyMock,
                 return_value={'1234/tcp': (1234, 'tcp')})
    cntr = Container(Image('unknown', max_wait=5.0))

    # When
    res = cntr.wait()

    assert res


# vim: et:sw=4:syntax=python:ts=4:
