# -*- coding: utf-8; -*-
import builtins
from typing import Optional, Tuple

import pytest

from dockerfixtures.container import FakeContainer, TimeOut, WaiterMixin


class WaiterMixinDerived(WaiterMixin):

    def __init__(self, address: str = 'localhost', *ports: Tuple[str, int], max_wait=None) -> None:
        self._address = address
        self._ports = ports
        self._max_wait = max_wait or 1.0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

    @property
    def address(self):
        return self._address

    @property
    def ports(self):
        return {'{port}/{proto}': (port, proto) for port, proto in self._ports}

    @property
    def max_wait(self):
        return self._max_wait


@pytest.fixture(params=(
    pytest.param(None, id='no max wait'),
    pytest.param(6.0, id='6.0s wait'),
))
def max_wait(request) -> Optional[float]:
    return request.param


@pytest.fixture(params=(
    pytest.param(True, id='pass ports to wait'),
    pytest.param(False, id='do not pass ports to wait'),
))
def pass_ports_to_wait(request):
    return request.param


@pytest.fixture(params=(
    pytest.param(((1234, 'tcp'), ), id='1234/tcp'),
))
def ports(request) -> Tuple[Tuple[int, str], ...]:
    return request.param


@pytest.fixture
def wait_ports(ports, pass_ports_to_wait) -> Tuple[Tuple[int, str], ...]:
    if pass_ports_to_wait:
        return ports
    return tuple()


@pytest.fixture(params=(
    pytest.param(WaiterMixinDerived, id='WaiterMixinDerived'),
    pytest.param(FakeContainer, id='FakeContainer'),
))
def waiter_class(request):
    return request.param


@pytest.fixture
def waiter_ports(ports, pass_ports_to_wait) -> Tuple[Tuple[int, str], ...]:
    if pass_ports_to_wait:
        return tuple()
    return ports


@pytest.fixture
def waiter(max_wait, waiter_ports, waiter_class):
    return waiter_class('localhost', *waiter_ports, max_wait=max_wait)


def test_waiter_mixin_wait_when_service_does_not_start_fast_enough(max_wait,
                                                                   mocker,
                                                                   wait_ports,
                                                                   waiter,
                                                                   ):
    # Given
    # Requirement: time_mock.side_effect[-1] - time_mock.side_effect[0] > max_wait
    time_mock = mocker.patch('dockerfixtures.container.time',
                             side_effect=[0.1, 0.2, 10.0, 10.0, 10.0])
    mocker.patch('dockerfixtures.container.socket',
                 side_effect=builtins.ConnectionError())

    # Ensure
    with pytest.raises(TimeOut):
        # When
        waiter.wait(*wait_ports, max_wait=max_wait)

    assert time_mock.call_count == 4


def test_waiter_mixin_wait_when_service_starts_fast_enough(mocker, wait_ports, waiter):
    # Given
    mocker.patch('dockerfixtures.container.socket')

    # When
    res = waiter.wait(*wait_ports, max_wait=1.0)

    # Then
    assert res


def test_waiter_mixin_as_context_manager_wait_when_service_does_not_start_fast_enough(max_wait,
                                                                                      mocker,
                                                                                      wait_ports,
                                                                                      waiter,
                                                                                      ):
    # Given
    # Requirement: time_mock.side_effect[-1] - time_mock.side_effect[0] > max_wait
    time_mock = mocker.patch('dockerfixtures.container.time',
                             side_effect=[0.1, 0.2, 10.0, 10.0, 10.0])
    mocker.patch('dockerfixtures.container.socket',
                 side_effect=builtins.ConnectionError())

    # Ensure
    with pytest.raises(TimeOut), waiter as self:
        # When
        self.wait(*wait_ports, max_wait=max_wait)

    assert time_mock.call_count == 4


def test_waiter_mixin_as_context_manager_wait_when_service_starts_fast_enough(mocker,
                                                                              wait_ports,
                                                                              waiter):
    # Given
    mocker.patch('dockerfixtures.container.socket')

    # When
    with waiter as self:
        res = self.wait(*wait_ports, max_wait=1.0)

    # Then
    assert res


# vim: et:sw=4:syntax=python:ts=4:
