# -*- coding: utf-8; -*-
import logging

import docker
import pytest

from dockerfixtures import container, image


# Set log leve to DEBUG to get some logs from the docker lib
logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture
def client():
    return docker.from_env()


@pytest.fixture
def netcat_port():
    return 9876


@pytest.fixture(scope='function')
def netcat(netcat_port):
    client = docker.from_env()
    yield from container.fixture(client,
                                 image.Image('subfuzion/netcat'),
                                 command=['nc', '-vl', str(netcat_port)],
                                 )


# vim: et:sw=4:syntax=python:ts=4:
