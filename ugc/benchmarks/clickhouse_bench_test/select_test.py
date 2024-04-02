import logging
from time import time
from uuid import uuid4

from faker import Faker
from clickhouse_driver import Client

from config import settings


def select_test():
    logging.info('\nInsert test running')

    fake: Faker = Faker()
    client = Client(
        host='test-clickhouse-node1',
        user=settings.clickhouse_username,
        password=settings.clickhouse_password)

    TRIES_COUNT: int = 1000
    # Get rows count
    get_rows_count_query = 'SELECT COUNT(*) FROM replica_db.player_progress'
    result = client.execute(get_rows_count_query)
    print(result)
    
    # start_time: float = time()

    # full_data_sql_query = 'SELECT * FROM replica_db.player_progress '


    # for _ in range(TRIES_COUNT):
    #     try:
    #         client.execute(query=full_data_sql_query)
    #     except Exception as e:
    #         logging.error(f'{e.__class__.__name__}:\n{str(e)=}')

    # selecting_time: float = time() - start_time
    # selecting_speed: float = round(selecting_time / TRIES_COUNT, 2)

    # print('Select speed: {:,} records/sec'.format(insertion_speed))
    # logging.info('Insertion speed: {:,} records/sec'.format(insertion_speed))


def main():
    try:
        select_test()
    except Exception as e:
        logging.error(
            f'Error raised during select_test.\n{e.__class__.__name__}:\n{str(e)}\n')
        raise e


if __name__ == '__main__':
    main()
