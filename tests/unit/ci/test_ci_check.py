# -*- coding: utf-8; -*-
from dockerfixtures.ci import is_containerized_ci


def test_is_containerized_ci(ci_environment):
    # Given

    # When
    result = is_containerized_ci()

    # Then
    assert result == ci_environment


# vim: et:sw=4:syntax=python:ts=4:
