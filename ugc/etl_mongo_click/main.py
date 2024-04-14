import json
import logging
from contextlib import closing

from pymongo import MongoClient, ASCENDING

from clickehouse_publisher import get_clickhouse_client
from config import settings
from constants import ASSOCIATION_COLLECTION_TO_SCHEMA, ASSOCIATION_COLLECTION_TO_CH_TABLE
from mongo_client import get_mongo_client


def convert_document_to_modeldata(document, colection_name):
    model_data_schema = ASSOCIATION_COLLECTION_TO_SCHEMA[colection_name]
    try:
        model_data = model_data_schema(**document)
    except Exception as e:
        logging.error(f'{e.__class__.__name__}:\n{str(e)=}')
        return None

    return model_data


def etl_data():
    with closing(get_mongo_client()) as mongo_client, closing(get_clickhouse_client()) as click_client:
        last_tables_updates_dt = {
            ch_table_name: None
            for ch_table_name in ASSOCIATION_COLLECTION_TO_CH_TABLE.values()
        }

        for ch_table_name in last_tables_updates_dt:
            last_update = click_client.execute(
                f'SELECT event_dt FROM shard.{ch_table_name} ORDER BY event_dt DESC LIMIT 1'
            )
            if last_update:
                last_tables_updates_dt[ch_table_name] = last_update[0][0]

        while True:
            for collection_name, schema in ASSOCIATION_COLLECTION_TO_SCHEMA:
                ch_table_name = ASSOCIATION_COLLECTION_TO_CH_TABLE[collection_name]
                ch_table_columns_as_str = ', '.join(schema.dict().keys())
                insert_sql_query = \
                    f'INSERT INTO shard_db.{ch_table_name} ({ch_table_columns_as_str}) VALUES'

                if last_tables_updates_dt[ch_table_name]:  # Если есть данные об обновлении
                    find_filter = {
                        'dt': {
                            '$gt': last_tables_updates_dt[ch_table_name]
                        }
                    }
                else:
                    find_filter = {}

                new_docs_batches = mongo_client.ugc[collection_name].find(
                    find_filter,
                    batch_size=settings.mongo_ch_etl_batch_size
                ).sort('dt', ASCENDING)

                if new_docs_batches:
                    for new_docs_batch in new_docs_batches:
                        objects_to_insert = [
                            list(convert_document_to_modeldata(doc).dict().values())
                            for doc in new_docs_batch
                        ]

                        try:
                            click_client.execute(
                                query=insert_sql_query,
                                params=objects_to_insert
                            )

                            # Выставляем новую дату последнего обновления
                            last_update_db = new_docs_batch[-1]['dt']
                            last_tables_updates_dt[ch_table_name] = last_update_db

                        except Exception as e:
                            logging.error(f'{e.__class__.__name__}:\n{str(e)=}')


if __name__ == '__main__':
    etl_data()
