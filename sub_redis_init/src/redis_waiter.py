from time import sleep
import logging

import redis

from core.config import settings


def wait_for_redis():
    logging.info('Run waiter for Redis')
    tries = 0
    sleep_time = 1
    factor = 2
    border_sleep_time = 10

    while True:
        try:
            tries += 1
            redis_session = redis.Redis(**settings.redis.conn_data)
            redis_session.get('some_key')
            logging.info('Succeed')
            break
        except Exception as e:
            logging.error(e.__class__.__name__)
            sleep_time = min(sleep_time * 2**factor, border_sleep_time)
            sleep(sleep_time)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='log.log',
        filemode='a'
    )

    wait_for_redis()
