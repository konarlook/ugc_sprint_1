import logging

import vertica_python


def create_infra():
    logging.info('Prepare to create databases')

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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_progress (
                user_id UUID NOT NULL,
                movie_id UUID NOT NULL,
                event_dt DateTime NOT NULL,
                view_progress INTEGER NOT NULL,
                movie_duration INTEGER NOT NULL
            );
            """)

    logging.info("Table successfully created")


def main():
    logging.basicConfig(
        level=logging.INFO,
        filename="log.log",
        filemode="a"
    )
    try:
        create_infra()
    except Exception as e:
        logging.error(f'{e.__class__.__name__}: \n {str(e)}')


if __name__ == '__main__':
    main()
