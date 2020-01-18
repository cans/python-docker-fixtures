# -*- coding: utf-8; -*-
import pytest

from dockerfixtures.container import Container
from dockerfixtures.image import Image


def test_container_remove_when_not_started():
    # Given
    cntr = Container(Image(''), startup_poll_interval=0.0)

    # Ensure
    with pytest.warns(RuntimeWarning, match='never.*started'):
        # When
        cntr.remove()


# vim: et:sw=4:syntax=python:ts=4:
