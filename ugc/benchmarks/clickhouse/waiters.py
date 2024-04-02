import logging

from clickhouse_driver import Client

from backoff import backoff
from config import settings


@backoff((ConnectionError,))
def wait_first_node():
    try:
        client = Client(host='test-clickhouse-node1',
                        user=settings.clickhouse_username,
                        password=settings.clickhouse_password)
        client.execute('SHOW DATABASES')
        logging.info("First node ready!")
        return True
    except Exception as e:
        logging.info(f'{e.__class__.__name__}')
        return None


@backoff((ConnectionError,))
def wait_second_node():
    try:
        client = Client(host='test-clickhouse-node2',
                        user=settings.clickhouse_username,
                        password=settings.clickhouse_password)
        client.execute('SHOW DATABASES')
        logging.info('Second node ready!')
        return True
    except Exception as e:
        logging.info(f'{e.__class__.__name__}')
        return None


@backoff((ConnectionError,))
def wait_third_node():
    try:
        client = Client(host='test-clickhouse-node3',
                        user=settings.clickhouse_username,
                        password=settings.clickhouse_password)
        client.execute('SHOW DATABASES')
        logging.info('Third node ready!')
        return True
    except Exception as e:
        logging.info(f'{e.__class__.__name__}')
        return None


def main():
    wait_first_node()
    wait_second_node()
    wait_third_node()


if __name__ == '__main__':
    main()
