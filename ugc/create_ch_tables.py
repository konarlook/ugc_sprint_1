from clickhouse_driver import Client


# ДОБАВИТЬ ИМПОРТ ПЕРЕМЕННЫХ ИЗ SETTINGS
def create_tables_for_first_node():
    client = Client(host='localhost', port=9000, user='admin', password='123')

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
        raise Exception

    replica_db_tables = client.execute('SHOW TABLES FROM replica_db')
    if replica_db_tables != [('click_event',), ('player_progress',), ('player_settings_event',)]:
        raise Exception


def create_tables_for_second_node():
    client = Client(host='localhost', port=9001, user='admin', password='123')

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
        raise Exception


def create_tables_for_third_node():
    client = Client(host='localhost', port=9002, user='admin', password='123')

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
        raise Exception


# def select_test():
#     first_client = Client(host='localhost', port=9002, user='admin', password='123')
#     first_client.execute(
#         "INSERT INTO replica_db.player_progress \
#         (user_id, movie_id, event_dt, view_progress, movie_duration) \
#         VALUES (\
#             '1c1884cc-17c8-4d6c-93c3-c4c385f468b5', \
#             '251fd098-0965-4c79-8ab6-81404f9f9e37', \
#             today(), \
#             123, \
#             456 \
#         )")

#     first_result = first_client.execute('SELECT * FROM replica_db.player_progress')

#     second_client = Client(host='localhost', port=9000, user='admin', password='123')
#     second_result = second_client.execute('SELECT * FROM shard_db.player_progress')

#     if first_result != second_result:
#         raise Exception


def main():
    create_tables_for_first_node()
    create_tables_for_second_node()
    create_tables_for_third_node()


if __name__ == '__main__':
    main()
