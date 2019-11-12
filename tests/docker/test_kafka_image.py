# -*- coding: utf-8; -*-
import functools
import json
import logging
import time

from kafka import errors, KafkaConsumer, KafkaProducer

from dockerfixtures import catalog
from dockerfixtures.container import Container


def test_container_from_kafka_image_all_defaults(client):
    topic = 'topic'
    message_count = 20
    max_attempts = 20
    with Container(catalog.PAPERLIB_KAFKA_2_3_1,
                   dockerclient=client,
                   max_wait=100,
                   # options={'ports': {'9092/tcp': 9092}, }
                   ) as cntr1, \
         Container(catalog.PAPERLIB_KAFKA_2_3_1,
                   dockerclient=client,
                   max_wait=100,
                   # options={'ports': {'9092/tcp': 9092}, }
                   ) as cntr2, \
         Container(catalog.PAPERLIB_KAFKA_2_3_1,
                   dockerclient=client,
                   max_wait=100,
                   # options={'ports': {'9092/tcp': 9092}, }
                   ) as cntr3:
        broker = '{}:9092'.format(cntr1.address)
        for attempt in range(1, max_attempts + 1):
            try:
                time.sleep(1.5)  # See https://github.com/docker-library/postgres/issues/146
                producer = KafkaProducer(bootstrap_servers=broker)
                logging.getLogger().info('Container reachable after %d try.', attempt)
                break
            except errors.NoBrokersAvailable:
                logging.getLogger().exception('Attempt %d failed !', attempt)
                if attempt == max_attempts:
                    raise

        for ndx in range(message_count):
            producer.send(topic, json.dumps({'hello': 'nanny {}'.format(ndx)}).encode('utf-8'))

        consumer = KafkaConsumer(bootstrap_servers=broker,
                                 value_deserializer=functools.patial(json.loads, encoding='utf-8'))
        consumer.subscribe([topic])
        for idx, message in enumerate(consumer):
            logging.getLogger().info(message)


# vim: et:sw=4:syntax=python:ts=4:
