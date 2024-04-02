import logging
from time import time

import vertica_python


def select_test():
    logging.info('Select test running')

    connection_info = {
        'host': 'vertica',
        'port': 5433,
        'user': 'dbadmin',
        'password': '',
        'database': 'docker',
        'autocommit': True,
    }

    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        get_rows_count_sql_query = 'SELECT COUNT(*) FROM player_progress'
        cursor.execute(get_rows_count_sql_query)
        rows_count = cursor.fetchall()[0][0]

        FULL_DATA_SQL_QUERY = 'SELECT * FROM player_progress '
        TRIES_COUNT: int = 5

        start_time: float = time()
        for _ in range(TRIES_COUNT):
            try:
                cursor.execute(FULL_DATA_SQL_QUERY)
            except Exception as e:
                logging.error(f'{e.__class__.__name__}:\n{str(e)=}')
                break

        selecting_time: float = time() - start_time
        rows_per_second: float = round(rows_count / (selecting_time / TRIES_COUNT), 2)

        logging.info('Select speed: {:,} records/sec'.format(rows_per_second))


def main():
    logging.basicConfig(
        level=logging.INFO,
        filename="log.log",
        filemode="a"
    )
    try:
        select_test()
    except Exception as e:
        logging.error(
            f'Error raised during select_test.\n{e.__class__.__name__}:\n{str(e)}\n')
        raise e


if __name__ == '__main__':
    main()
