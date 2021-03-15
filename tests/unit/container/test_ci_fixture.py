# -*- coding: utf-8; -*-
import pytest

from dockerfixtures import container, image


@pytest.mark.parametrize(('ci_environment', ), (
    pytest.param(('CI', 'CIRCLECI'), id='within circleci'),
), indirect=('ci_environment', ))
def test_ci_fixture_forwards_arguments(mocker, ci_environment, client):
    # Given
    ContainerClass = mocker.patch('dockerfixtures.container.FakeContainer')
    cmd = ['abc', 'def']
    env = dict()
    img = image.Image('')
    interval = 567.8
    maxwait = 123.4
    opts = dict()
    ci_address = 'whatever'
    ports = ((5432, 'tcp', ), (5432, 'unix', ), )

    # When
    next(container.ci_fixture(client,
                              img,
                              *ports,
                              command=cmd,
                              environment=env,
                              max_wait=maxwait,
                              options=opts,
                              readyness_poll_interval=interval,
                              ci_address=ci_address,
                              ))

    # Then
    ContainerClass.assert_called_once_with(ci_address, *ports)
    # Should we wait or assume the CI does its work properly only run
    # tests once the containers are ready ?
    # ContainerClass().__enter__().wait.assert_called_once_with(*ports,
    #                                                           readyness_poll_interval=interval,
    #                                                           max_wait=maxwait)


@pytest.mark.parametrize(('ci_environment', ), (
    pytest.param(('CI', 'CIRCLECI'), id='within circleci'),
), indirect=('ci_environment', ))
def test_ci_fixture_is_fake_container_when_ci_defined(ci_environment, client):
    # Given
    cmd = ['abc', 'def']
    env = dict()
    img = image.Image('')
    interval = 567.8
    maxwait = 123.4
    opts = dict()
    ports = ((5432, 'tcp', ), (5432, 'unix', ), )

    # When
    cntr = next(container.ci_fixture(client,
                                     img,
                                     *ports,
                                     command=cmd,
                                     environment=env,
                                     max_wait=maxwait,
                                     options=opts,
                                     readyness_poll_interval=interval,
                                     ))
    # Then
    assert isinstance(cntr, container.FakeContainer)


# vim: et:sw=4:syntax=python:ts=4:
