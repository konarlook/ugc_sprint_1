import logging

from clickhouse_driver import Client

from config import settings


def get_clickhouse_client():
    logging.info('Prepare to create Clickhouse client')

    clickhouse_client = Client(
        host='clickhouse-node1',
        user=settings.clickhouse_username,
        password=settings.clickhouse_password
    )

    logging.info('Clickhouse client created!')

    return clickhouse_client
