# -*- coding: utf-8; -*-
import logging

import docker
import pytest


# Set log leve to DEBUG to get some logs from the docker lib
logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture
def client():
    return docker.from_env()


# vim: et:sw=4:syntax=python:ts=4:
