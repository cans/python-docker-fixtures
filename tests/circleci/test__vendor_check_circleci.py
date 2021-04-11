# -*- coding: utf-8; -*-
import json
import os
from urllib.request import urlopen

import pytest

from dockerfixtures.ci import __vendor_check_circleci


@pytest.fixture
def environ(monkeypatch):
    buildnum = 360
    if 'CIRCLE_BUILD_NUM' not in os.environ:
        monkeypatch.setenv('CIRCLE_BUILD_NUM', buildnum)
    if 'CIRCLE_BUILD_URL' not in os.environ:
        monkeypatch.setenv('CIRCLE_BUILD_URL',
                           f'https://circleci.com/gh/cans/python-docker-fixtures/{buildnum}')
    return os.environ


def test___vendor_check_circleci(environ):
    # Given
    url = ('https://circleci.com/api/v2/project/gh/cans/python-docker-fixtures/job/{}'
           .format(environ['CIRCLE_BUILD_NUM'])
           )
    with urlopen(url) as response:
        response_data = json.load(response)

    # When
    result = __vendor_check_circleci(environ)

    # Then
    assert result == (response_data['executor']['type'] == 'docker')


# vim: et:sw=4:syntax=python:ts=4:
