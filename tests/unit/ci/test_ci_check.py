# -*- coding: utf-8; -*-
from unittest.mock import Mock

from dockerfixtures import ci


def test_is_containerized_ci(ci_environment, monkeypatch):
    # Given
    mocked_vendor_check = Mock(return_value=ci_environment)
    monkeypatch.setitem(ci.__VENDOR_CHECKS, 'CIRCLECI', mocked_vendor_check)

    # When
    result = ci.is_containerized_ci()

    # Then
    assert result == ci_environment


# vim: et:sw=4:syntax=python:ts=4:
