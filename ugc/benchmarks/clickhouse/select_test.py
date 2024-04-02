import logging
from time import time

from clickhouse_driver import Client

from config import settings


def select_test():
    logging.info('\Select test running')

    client = Client(
        host='test-clickhouse-node1',
        user=settings.clickhouse_username,
        password=settings.clickhouse_password)

    get_rows_count_sql_query = 'SELECT COUNT(*) FROM replica_db.player_progress'
    rows_count = client.execute(get_rows_count_sql_query)[0][0]

    FULL_DATA_SQL_QUERY = 'SELECT * FROM replica_db.player_progress '
    TRIES_COUNT: int = 5
    start_time: float = time()
    for _ in range(TRIES_COUNT):
        try:
            client.execute(query=FULL_DATA_SQL_QUERY)
        except Exception as e:
            logging.error(f'{e.__class__.__name__}:\n{str(e)=}')
            break

    selecting_time: float = time() - start_time
    rows_per_second: float = round(rows_count / (selecting_time / TRIES_COUNT), 2)

    logging.info('Select speed: {:,} records/sec'.format(rows_per_second))


def main():
    try:
        select_test()
    except Exception as e:
        logging.error(
            f'Error raised during select_test.\n{e.__class__.__name__}:\n{str(e)}\n')
        raise e


if __name__ == '__main__':
    main()
