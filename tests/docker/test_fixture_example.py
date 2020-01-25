# -*- coding: utf-8; -*-
import socket


def test_fixture_example(netcat, netcat_port):
    # Given

    # When
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((netcat.address, netcat_port))

    # Then
    assert True  # Must be reached


# vim: et:sw=4:syntax=python:ts=4:
