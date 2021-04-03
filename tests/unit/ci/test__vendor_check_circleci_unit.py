# -*- coding: utf-8; -*-
import io
import json
from unittest.mock import Mock

import pytest

from dockerfixtures.ci import __vendor_check_circleci


@pytest.fixture
def environment(token):
    buildnum = 360
    env = {'CIRCLE_BUILD_NUM': buildnum,
           'CIRCLE_BUILD_URL': f'https://circleci.com/gh/cans/python-docker-fixtures/{buildnum}',
           }
    if token:
        env['CIRCLECI_API_TOKEN'] = token
    return env


@pytest.fixture(params=(
    pytest.param('docker', id='docker executor'),
    pytest.param('machine', id='machine executor'),
    pytest.param('macos', id='macos executor'),
    # pytest.param('', id=' executor'),
))
def executor_type(request):
    return request.param


@pytest.fixture
def expected_result(executor_type):
    return 'docker' == executor_type


@pytest.fixture
def response(executor_type, monkeypatch):
    response_data = {'executor': {'type': executor_type}, }
    response = io.StringIO(json.dumps(response_data))
    monkeypatch.setattr('dockerfixtures.ci.urlopen', Mock(return_value=response))
    return response_data


@pytest.fixture(params=(
    pytest.param('azerty', id='with API token'),
    pytest.param(False, id='without API token'),
))
def token(request):
    return request.param


@pytest.fixture
def url(environment):
    return ('https://circleci.com/api/v2/project/gh/cans/python-docker-fixtures/job/'
            '{CIRCLE_BUILD_NUM}'.format(**environment)
            )


def test___vendor_check_circleci(environment, expected_result, response, ):
    # Given

    # When
    result = __vendor_check_circleci(environment)

    # Then
    assert result == expected_result
    assert not result or 'docker' == response['executor']['type']


def test___vendor_check_circleci_request_has_token_header(environment,
                                                          expected_result,
                                                          monkeypatch,
                                                          response,
                                                          token,
                                                          url):
    # Given
    request_mock = Mock()
    monkeypatch.setattr('dockerfixtures.ci.Request', request_mock)
    kwargs = {'headers': {},
              'method': 'GET',
              }
    if token:
        kwargs['headers']['Circle-Token'] = token

    # When
    result = __vendor_check_circleci(environment)

    # Then
    assert result == expected_result
    assert not result or 'docker' == response['executor']['type']
    request_mock.assert_called_once_with(url, **kwargs)


# vim: et:sw=4:syntax=python:ts=4:
