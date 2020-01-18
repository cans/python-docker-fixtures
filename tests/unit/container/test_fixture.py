# -*- coding: utf-8; -*-
from dockerfixtures import container, image


def test_fixture_forwards_arguments(mocker):
    # Given
    Container = mocker.patch('dockerfixtures.container.Container')
    env = dict()
    img = image.Image('')
    interval = 567.8
    maxwait = 123.4
    opts = dict()
    ports = ((5432, 'tcp', ), (5432, 'unix', ), )

    # When
    next(container.fixture(img,
                           *ports,
                           environment=env,
                           max_wait=maxwait,
                           options=opts,
                           readyness_poll_interval=interval,
                           ))

    # Then
    Container.assert_called_once_with(img, options=opts, environment=env)
    Container().__enter__().wait.assert_called_once_with(*ports,
                                                         readyness_poll_interval=interval,
                                                         max_wait=maxwait)


# vim: et:sw=4:syntax=python:ts=4:
