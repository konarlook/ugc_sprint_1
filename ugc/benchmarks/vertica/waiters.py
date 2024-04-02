import logging
import vertica_python

from backoff import backoff


@backoff((ConnectionError,), attempts=100)
def wait_vertica():
    try:
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

            query = """
                select table_name from v_catalog.tables
                """

            cursor.execute(operation=query)

        return True
    except Exception as e:
        logging.info(f'{e.__class__.__name__}')
        return None


def main():
    wait_vertica()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename="log.log",
        filemode="a"
    )
    main()
