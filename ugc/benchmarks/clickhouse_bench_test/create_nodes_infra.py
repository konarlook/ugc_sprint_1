import logging

from clickhouse_driver import Client

from config import settings


def create_tables_for_first_node():
    logging.info('Prepare to create databases on first node')
    client = Client(host='test-clickhouse-node1',
                    user=settings.clickhouse_username,
                    password=settings.clickhouse_password)
    logging.info('Client created')

    client.execute('CREATE DATABASE IF NOT EXISTS shard_db;')
    client.execute('CREATE DATABASE IF NOT EXISTS replica_db;')

    # create player_progress table
    client.execute(
        "CREATE TABLE IF NOT EXISTS shard_db.player_progress "
        "(user_id UUID, movie_id UUID, event_dt DateTime, view_progress Int64, movie_duration Int64) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/player_progress', 'replica_1') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")

    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.player_progress "
        "(user_id UUID, movie_id UUID, event_dt DateTime, view_progress Int64, movie_duration Int64) "
        "ENGINE = Distributed('ugc_cluster', '', player_progress, rand());")

    # create player_settings_event table
    client.execute(
        "CREATE TABLE IF NOT EXISTS shard_db.player_settings_event "
        "(user_id UUID, movie_id UUID, event_dt DateTime, event_type String) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/player_settings_event', 'replica_1') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.player_settings_event "
        "(user_id UUID, movie_id UUID, event_dt DateTime, event_type String) "
        "ENGINE = Distributed('ugc_cluster', '', player_settings_event, rand());")

    # # create player_settings_event click_event
    client.execute(
        "CREATE TABLE IF NOT EXISTS shard_db.click_event "
        "(user_id UUID, event_dt DateTime, current_url String NULL, destination_url String NULL) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/click_event', 'replica_1') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.click_event "
        "(user_id UUID, event_dt DateTime, current_url String NULL, destination_url String NULL) "
        "ENGINE = Distributed('ugc_cluster', '', click_event, rand());")

    shard_db_tables = client.execute('SHOW TABLES FROM shard_db')
    if shard_db_tables != [('click_event',), ('player_progress',), ('player_settings_event',)]:
        logging.error("Required tables don't exist on first node (shard_db)!")
        raise Exception

    replica_db_tables = client.execute('SHOW TABLES FROM replica_db')
    if replica_db_tables != [('click_event',), ('player_progress',), ('player_settings_event',)]:
        logging.error("Required tables don't exist on first node (replica_db)!")
        raise Exception

    logging.info("Tables successfully created on first node!")
    print(client.execute('SHOW DATABASES'))
    print(client.execute('SHOW TABLES FROM shard_db'))
    print(client.execute('SHOW TABLES FROM replica_db'))


def create_tables_for_second_node():
    logging.info('Prepare to create databases on second node')
    client = Client(host='test-clickhouse-node2',
                    user=settings.clickhouse_username,
                    password=settings.clickhouse_password)
    logging.info('Client created')

    client.execute('CREATE DATABASE IF NOT EXISTS replica_db;')

    # create player_progress table
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.player_progress "
        "(user_id UUID, movie_id UUID, event_dt DateTime, view_progress Int64, movie_duration Int64) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/player_progress', 'replica_2') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")

    # create player_settings_event table
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.player_settings_event "
        "(user_id UUID, movie_id UUID, event_dt DateTime, event_type String) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/player_settings_event', 'replica_2') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")

    # create click_event table
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.click_event "
        "(user_id UUID, event_dt DateTime, current_url String NULL, destination_url String NULL) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/click_event', 'replica_2') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")

    tables = client.execute('SHOW TABLES FROM replica_db')
    if tables != [('click_event',), ('player_progress',), ('player_settings_event',)]:
        logging.error("Required tables don't exist on second node (replica_db)!")
        raise Exception

    logging.info("Tables successfully created on second node!")
    print(client.execute('SHOW DATABASES'))
    print(client.execute('SHOW TABLES FROM replica_db'))


def create_tables_for_third_node():
    logging.info('Prepare to create databases on third node')
    client = Client(host='test-clickhouse-node3',
                    user=settings.clickhouse_username,
                    password=settings.clickhouse_password)
    logging.info('Client created')

    client.execute('CREATE DATABASE IF NOT EXISTS replica_db;')

    # create player_progress table
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.player_progress "
        "(user_id UUID, movie_id UUID, event_dt DateTime, view_progress Int64, movie_duration Int64) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/player_progress', 'replica_3') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")

    # create player_settings_event table
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.player_settings_event "
        "(user_id UUID, movie_id UUID, event_dt DateTime, event_type String) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/player_settings_event', 'replica_3') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")

    # create click_event table
    client.execute(
        "CREATE TABLE IF NOT EXISTS replica_db.click_event "
        "(user_id UUID, event_dt DateTime, current_url String NULL, destination_url String NULL) "
        "Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/click_event', 'replica_3') "
        "PARTITION BY toYYYYMMDD(event_dt) ORDER BY event_dt;")

    tables = client.execute('SHOW TABLES FROM replica_db')
    if tables != [('click_event',), ('player_progress',), ('player_settings_event',)]:
        logging.error("Required tables don't exist on third node (replica_db)!")
        raise Exception

    logging.info("Tables successfully created on third node!")
    print(client.execute('SHOW DATABASES'))
    print(client.execute('SHOW TABLES FROM replica_db'))


def main():
    try:
        create_tables_for_first_node()
        create_tables_for_second_node()
        create_tables_for_third_node()
    except Exception as e:
        logging.error(f'{e.__class__.__name__}: \n {str(e)}')


if __name__ == '__main__':
    main()
