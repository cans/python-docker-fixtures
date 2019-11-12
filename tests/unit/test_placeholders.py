# -*- coding: utf-8; -*-
import pytest

from dockerfixtures import placeholders
from dockerfixtures.placeholders import _Placeholder, ContainerID, ContainerIDType


@pytest.mark.parametrize('builder', [_Placeholder, type(ContainerID), ContainerIDType])
@pytest.mark.parametrize('typename', [str(ContainerID)])
def test_placeholder_is_a_singleton(builder, typename):
    """Ensures there is no way to have two instances of the ContainerIDType
    """
    # When
    placeholder = builder(typename)

    # Then
    assert placeholder is ContainerID
    assert type(placeholder) is type(ContainerID)


@pytest.mark.parametrize('placeholder', [placeholders.ContainerID, placeholders.ImageID])
def test_placeholder_repr_works(placeholder):
    # When
    str_value = "{}".format(repr(placeholder))

    # Then
    assert str_value == '{}.{}'.format(placeholders.__name__, str(placeholder))


# vim: et:sw=4:syntax=python:ts=4:
