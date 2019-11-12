# -*- coding: utf-8; -*-
"""Provides a catalog of pre-defined docker images.
"""
from .image import Image


__PG_ENV = {'POSTGRES_PASSWORD': '',
            'POSTGRES_DB': 'postgres',
            'POSTGRES_USER': 'postgres',
            'POSTGRES_INITDB_ARGS': None,
            'POSTGRES_INITDB_WALDIR': None,
            'PGDATA': None,
            }
PG_12 = Image('postgres', tag='12', environment=__PG_ENV)
PG_12_ALPINE = Image('postgres', tag='12-alpine', environment=__PG_ENV)
PG_11 = Image('postgresql', tag='11', environment=__PG_ENV)
PG_11_ALPINE = Image('postgres', tag='11-alpine', environment=__PG_ENV)
PG_10 = Image('postgres', tag='10', environment=__PG_ENV)
PG_10_ALPINE = Image('postgres', tag='10-alpine', environment=__PG_ENV)
PG_96 = Image('postgres', tag='9.6', environment=__PG_ENV)
PG_96_ALPINE = Image('postgres', tag='9.6-alpine', environment=__PG_ENV)

__KAFKA_ENV = {'KAFKA_ADVERTISED_LISTENERS': 'LISTENERS_DOCKER_INTERNAL://${DOCKER_HOST_NAME}:9092,LISTENERS_DOCKER_EXTERNAL://${DOCKER_HOST_IP:-locahost}:9092',
               'KAFKA_LISTENER_SECURITY_PROTOCOL_MAP': 'LISTENER_DOCKER_INTERNAL:PLAINTEXT,LISTENER_DOCKER_EXTERNAL:PLAINTEXT',
               'KAFKA_BROKER_ID': 1,
               }
CONFLUENT_KAFKA_5_0_0 = Image('confluentinc/kafka', tag='5.0.0', environment=__KAFKA_ENV)

__PAPERLIB_KAFKA_ENV = {}
PAPERLIB_KAFKA_LATEST = Image('paperlib/kafka', tag='latest', environment=__PAPERLIB_KAFKA_ENV)
PAPERLIB_KAFKA_2_3_1 = Image('paperlib/kafka', tag='2.3.1', environment=__PAPERLIB_KAFKA_ENV)
PAPERLIB_KAFKA_2_3_1_ALPINE = Image('paperlib/kafka', tag='2.3.1-alpine', environment=__PAPERLIB_KAFKA_ENV)


# vim: et:sw=4:syntax=python:ts=4:
