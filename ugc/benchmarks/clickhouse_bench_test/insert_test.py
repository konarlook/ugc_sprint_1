import logging
from time import time
from uuid import uuid4
from datetime import datetime as dt

from faker import Faker
from clickhouse_driver import Client

from config import settings


def insert_test():
    logging.info('\nInsert test running')

    fake: Faker = Faker()
    client = Client(
        host='test-clickhouse-node1',
        user=settings.clickhouse_username,
        password=settings.clickhouse_password)

    BATCH_SIZE: int = 5  # 10000
    BATCHES: int = 3  # 1000
    TOTAL_RECORDS: float = BATCH_SIZE * BATCHES

    start_time: float = time()

    sql_query = \
        'INSERT INTO replica_db.player_progress \
        (user_id, movie_id, event_dt, view_progress, movie_duration) VALUES'

    for _ in range(BATCHES):
        print(_)
        # rows_to_insert = [
        #     (uuid4(),
        #      uuid4(),
        #      fake.date_time_between(start_date="-1y", end_date="now"),
        #      fake.random_int(min=0, max=1000),
        #      fake.random_int(min=1001, max=5000))
        #     for _ in range(BATCH_SIZE)
        # ]
        rows_to_insert = [
            [
                '1c1884cc-17c8-4d6c-93c3-c4c385f468b5',
                '251fd098-0965-4c79-8ab6-81404f9f9e37',
                dt.now(),
                123,
                456
            ]
            for _ in range(BATCH_SIZE)
        ]
        # rows_to_insert = [
        #     [uuid4(),
        #      uuid4(),
        #      fake.date_time_between(start_date="-1y", end_date="now"),
        #      fake.random_int(min=0, max=1000),
        #      fake.random_int(min=1001, max=5000)]
        #     for _ in range(BATCH_SIZE)
        # ]

        try:
            client.execute(
                query=sql_query,
                params=rows_to_insert)
        except Exception as e:
            logging.error(f'{e.__class__.__name__}:\n{str(e)=}')

    x = client.execute('SELECT * FROM replica_db.player_progress')
    print(x)

    insertion_time: float = time() - start_time
    insertion_speed: float = round(TOTAL_RECORDS / insertion_time, 2)

    print('Insertion speed: {:,} records/sec'.format(insertion_speed))
    logging.info('Insertion speed: {:,} records/sec'.format(insertion_speed))


def main():
    try:
        insert_test()
    except Exception as e:
        logging.error(
            f'Error raised during insert_test.\n{e.__class__.__name__}:\n{str(e)}\n')
        raise e


if __name__ == '__main__':
    main()
