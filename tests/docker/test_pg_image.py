# -*- coding: utf-8; -*-
import secrets
import subprocess

import pytest

from dockerfixtures import catalog
from dockerfixtures.ci import is_containerized_ci
from dockerfixtures.container import Container


@pytest.mark.skipif(is_containerized_ci(), reason='In a containerized CI environment')
def test_container_from_pg_image_all_defaults(client):
    env = {**catalog.PG_11.default_environment, 'POSTGRES_PASSWORD': secrets.token_urlsafe()}
    with Container(catalog.PG_11, dockerclient=client, max_wait=100, environment=env) as cntr:
        cntr.wait((5432, 'tcp'), max_wait=10.0)
        # time.sleep(1.5)  # See https://github.com/docker-library/postgres/issues/146
        subprocess.check_call(['docker', 'exec', '-i', cntr.id,
                               'psql',
                               '-U', catalog.PG_10.default_environment['POSTGRES_USER'],
                               # '-d', catalog.PG_10.default_environment['POSTGRES_DB'],
                               '-c', 'SELECT 1'])


# vim: et:sw=4:syntax=python:ts=4:
