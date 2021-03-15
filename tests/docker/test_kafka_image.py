# -*- coding: utf-8; -*-
import json
import logging

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

from dockerfixtures import catalog
from dockerfixtures.container import Container


def test_container_from_kafka_image_all_defaults(client):
    topic = 'topic'
    message_count = 20

    with Container(catalog.PAPERLIB_KAFKA_2_3_1,
                   dockerclient=client,
                   max_wait=100,
                   options={'network_mode': 'host',
                            }
                   ) as cntr:
        broker = '{}:9092'.format(cntr.address)
        # Wait for the container to be ready
        cntr.wait((9092, 'tcp'), readyness_poll_interval=0.5)

        # Create a topic to publish messages to
        kafka = KafkaAdminClient(bootstrap_servers=broker)
        topics = []
        topics.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
        kafka.create_topics(topics)

        # Produce a few message
        producer = KafkaProducer(bootstrap_servers=broker, acks=0)

        for ndx in range(message_count):
            producer.send(topic, json.dumps({'hello': 'nanny {}'.format(ndx)}).encode('utf-8'))

        # Make sure the messages were produced by consuming them
        consumer = KafkaConsumer(auto_offset_reset='earliest',
                                 bootstrap_servers=broker,
                                 consumer_timeout_ms=5000,
                                 # request_timeout_ms=5000, # 5 seconds max.
                                 value_deserializer=json.loads)
        consumer.subscribe([topic])
        for idx, message in enumerate(consumer):
            logging.getLogger().info(message)
        assert idx > 0


# vim: et:sw=4:syntax=python:ts=4:
