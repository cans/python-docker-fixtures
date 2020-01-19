# -*- coding: utf-8; -*-
import pytest

from dockerfixtures.container import _port, UnsupportedNetworkProtocol


@pytest.mark.parametrize('port, expected',
                         [('1234', (1234, 'tcp')),
                          ('1234/tcp', (1234, 'tcp')),
                          ('1234/udp', (1234, 'udp')),
                          ('1234/', (1234, 'tcp')),
                          ])
def test__port(port, expected):
    # When
    res = _port(port)

    # Then
    assert res == expected


def test__port_raises_when_protocol_is_unknown():
    # Ensure
    with pytest.raises(UnsupportedNetworkProtocol):
        _port('1234/udix')


# vim: et:sw=4:syntax=python:ts=4:
