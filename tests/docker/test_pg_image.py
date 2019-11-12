# -*- coding: utf-8; -*-
import logging
import subprocess
import time

from dockerfixtures import catalog
from dockerfixtures.container import Container


def test_container_from_pg_image_all_defaults(client):
    max_attempts = 10
    with Container(catalog.PG_10, dockerclient=client, max_wait=100) as cntr:
        for attempt in range(max_attempts):
            attempt += 1
            try:
                time.sleep(1.5)  # See https://github.com/docker-library/postgres/issues/146
                subprocess.check_call(['docker', 'exec', '-i', cntr.id,
                                       'psql',
                                       '-U', catalog.PG_10.default_environment['POSTGRES_USER'],
                                       # '-d', catalog.PG_10.default_environment['POSTGRES_DB'],
                                       '-c', 'SELECT 1'])
                logging.getLogger().info('Container reachable after %d try.', attempt)
                break
            except subprocess.CalledProcessError:
                logging.getLogger().warning('Attempt %d failed !', attempt)
                if attempt + 1 == max_attempts:
                    raise


# vim: et:sw=4:syntax=python:ts=4:
