# -*- coding: utf-8; -*-
import pytest

from dockerfixtures.container import Service


@pytest.mark.parametrize(('attr', ), (
    pytest.param('address', id='address attribute'),
    pytest.param('max_wait', id='max_wait attribute'),
    pytest.param('ports', id='ports attribute'),
    pytest.param('readyness_poll_interval', id='readyness_poll_interval attribute'),
))
def test_service_raises_not_implemented(attr):
    # Given
    service = Service()

    # Ensure
    with pytest.raises(NotImplementedError):
        # When
        getattr(service, attr)


# vim: et:sw=4:syntax=python:ts=4:
