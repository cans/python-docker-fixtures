# -*- coding: utf-8; -*-
import socket

import pytest

from dockerfixtures.ci import is_containerized_ci


@pytest.mark.skipif(is_containerized_ci(), reason='In a containerized CI environment')
def test_fixture_example(netcat, netcat_port):
    # Given

    # When
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((netcat.address, netcat_port))

    # Then
    assert True  # Must be reached


@pytest.mark.skipif(is_containerized_ci(), reason='In a containerized CI environment')
def test_ci_fixture_example_when_not_in_ci(netcat, netcat_port):
    # Given

    # When
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((netcat.address, netcat_port))

    # Then
    assert True  # Must be reached


# vim: et:sw=4:syntax=python:ts=4:
