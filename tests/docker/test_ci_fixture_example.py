# -*- coding: utf-8; -*-
"""Example of using dockerfixtures outside or within a CI environment

The same fixture here works the same whether the CI environment
that provide the docker images for you
"""
import socket

import pytest

from dockerfixtures.ci import is_containerized_ci
from dockerfixtures.container import Container, FakeContainer


@pytest.mark.skipif(not is_containerized_ci(), reason='Not in a containerized CI environment')
def test_ci_fixture_example_when_in_containerized_ci(ci_netcat, netcat_port):
    # Given

    # When
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ci_netcat.address, netcat_port))

    # Then
    assert isinstance(ci_netcat, FakeContainer)


@pytest.mark.skipif(is_containerized_ci(), reason='In a containerized CI environment')
def test_ci_fixture_example_when_not_in_containerized_ci(ci_netcat, netcat_port):
    # Given

    # When
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ci_netcat.address, netcat_port))

    # Then
    assert isinstance(ci_netcat, Container)


# vim: et:sw=4:syntax=python:ts=4:
