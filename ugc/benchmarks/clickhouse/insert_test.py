import logging
from time import time
from uuid import uuid4

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

    BATCH_SIZE: int = 10000
    BATCHES: int = 15
    TOTAL_RECORDS: float = BATCH_SIZE * BATCHES

    start_time: float = time()

    sql_query = \
        'INSERT INTO replica_db.player_progress \
        (user_id, movie_id, event_dt, view_progress, movie_duration) VALUES'

    for _ in range(BATCHES):
        rows_to_insert = [
            (uuid4(),
             uuid4(),
             fake.date_time_between(start_date="-1y", end_date="now"),
             fake.random_int(min=0, max=1000),
             fake.random_int(min=1001, max=5000))
            for _ in range(BATCH_SIZE)
        ]

        try:
            client.execute(query=sql_query, params=rows_to_insert)
        except Exception as e:
            logging.error(f'{e.__class__.__name__}:\n{str(e)=}')
            break

    insertion_time: float = time() - start_time
    insertion_speed: float = round(TOTAL_RECORDS / insertion_time, 2)

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
