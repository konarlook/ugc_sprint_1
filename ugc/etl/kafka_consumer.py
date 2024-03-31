import logging

from kafka import KafkaConsumer


def get_kafka_consumer():
    logging.info('Prepare to create KafkaConsumer')

    kafka_consumer = KafkaConsumer(
        'player_progress',
        'player_settings_event',
        'click_event',
        bootstrap_servers=['kafka-0:9092'],
        auto_offset_reset='earliest',
        group_id='ETL_to_Clickhouse',
    )
    logging.info('KafkaConsumer created')

    return kafka_consumer