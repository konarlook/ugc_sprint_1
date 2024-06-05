from time import sleep
from http import HTTPStatus
import logging

import requests
import redis

from core.config import settings
from schemas.user_subscription import UserSubscriptionSchema

from uuid import uuid4
from random import randint


def main():
    tries = 0
    sleep_time = 1
    factor = 2
    border_sleep_time = 10

    while True:
        try:
            tries += 1

            res = requests.get(settings.billing.full_url)
            if res != HTTPStatus.OK:
                logging('Billing service error')
                sleep_time = min(sleep_time * 2**factor, border_sleep_time)
                sleep(sleep_time)
                continue

            res_data = res.json()

            redis_session = redis.Redis(**settings.redis.conn_data)

            for sub_data in res_data:
                user_sub_model = UserSubscriptionSchema(**sub_data)

                status = redis_session.set(
                    user_sub_model.user_id,
                    user_sub_model.subscription_id,
                    user_sub_model.time
                )

                if status is not True:
                    raise ValueError(f"Can't save data for user {user_sub_model.user_id}")
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

    main()
