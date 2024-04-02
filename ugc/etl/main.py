import json
import logging

from config import settings
from clickehouse_publisher import get_clickhouse_client
from kafka_consumer import get_kafka_consumer
from constants import ASSOCIATION_TOPIC_TO_SCHEMA


def convert_msg_to_modeldata(message_value, topic_name):
    model_data_schema = ASSOCIATION_TOPIC_TO_SCHEMA[topic_name]
    try:
        model_data = model_data_schema.model_validate(message_value)
    except Exception as e:
        logging.error(f'{e.__class__.__name__}:\n{str(e)=}')
        return None

    return model_data


def consume_messages(consumer):
    topics_data = {
        'player_progress': {
            'message_count': 0,
            'rows_to_insert': [],
        },
        'player_settings_event': {
            'message_count': 0,
            'rows_to_insert': [],
        },
        'click_event': {
            'message_count': 0,
            'rows_to_insert': [],
        },
    }

    for message in consumer:
        topic_name = message.topic
        logging.info(f'Get message from {topic_name}')
        message_value = json.loads(message.value.decode('ascii'))

        if not isinstance(message_value, dict):
            logging.error(
                'Message value should be Dict instance!'
                f'{topic_name}:\n{message_value}'
            )
            continue

        model_data = convert_msg_to_modeldata(message_value, topic_name)
        if model_data is None:
            continue

        row_to_insert = list(dict(model_data).values())

        topics_data[message.topic]['rows_to_insert'].append(row_to_insert)
        topics_data[message.topic]['message_count'] += 1
        logging.info(f'Messages count {topics_data[message.topic]["message_count"]}')

        if topics_data[message.topic]['message_count'] >= settings.kafka_ch_etl_batch_size:
            logging.info(f'Prepare to bulk insert into {topic_name!r} table')
            topics_data[message.topic]['message_count'] = 0

            table_columns_as_str = ', '.join(dict(model_data).keys())
            sql_query = \
                f'INSERT INTO shard_db.{topic_name} ({table_columns_as_str}) VALUES'

            clickhouse_client = get_clickhouse_client()
            try:
                clickhouse_client.execute(
                    query=sql_query,
                    params=topics_data[message.topic]['rows_to_insert'])

                topics_data[message.topic]['rows_to_insert'] = []
            except Exception as e:
                logging.error(f'{e.__class__.__name__}:\n{str(e)=}')


if __name__ == '__main__':
    consumer = get_kafka_consumer()
    consume_messages(consumer)
