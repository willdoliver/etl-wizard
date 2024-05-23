import traceback, logging
import time
from datetime import datetime
from sqlalchemy import MetaData, create_engine

from api.helpers.logger_message_helper import LoggerMessageHelper
from api.repositories.etl_repository import ETLRepository
from dotenv import load_dotenv

load_dotenv()

class ETLController():

    def __init__(self):
        self.log_file = 'logs/log_etl_' + datetime.now().strftime("%Y_%m_%d") + '.log'

    def sync_data(self, db_name, tables):
        LoggerMessageHelper.log_message(self.log_file, 'Sync Data Started')

        tables_to_clone = []
        try:
            database_tables = ETLRepository.get_all_tables(db_name)

            if tables != 'all':
                tables_requested = tables.split(',')
                for table in tables_requested:
                    if table in database_tables:
                        tables_to_clone.append(table)
            else:
                tables_to_clone = database_tables

            source_engine = create_engine(ETLRepository.get_source_engine(db_name))
            target_engine = create_engine(ETLRepository.get_target_engine(db_name))

            source_metadata = MetaData()
            target_metadata = MetaData()

            for table_name in tables_to_clone:
                start_time = time.time()
                LoggerMessageHelper.log_message(self.log_file, f"cloninig table {table_name}")

                target_metadata.reflect(bind=target_engine)

                if table_name in target_metadata.tables:
                    target_table = target_metadata.tables[table_name]
                    target_table.drop(target_engine)
                    LoggerMessageHelper.log_message(self.log_file, f"Dropped existing table '{table_name}' in target database.")

                source_metadata.reflect(bind=source_engine, only=[table_name])
                source_table = source_metadata.tables.get(table_name)
                LoggerMessageHelper.log_message(self.log_file, f"Reflected Table: {source_table}")

                source_table.tometadata(target_metadata)
                target_metadata.create_all(target_engine)
                LoggerMessageHelper.log_message(self.log_file, f"Created table '{table_name}' in target database.")

                with source_engine.connect() as source_conn, target_engine.connect() as target_conn:
                    select_query = source_table.select()
                    result = source_conn.execute(select_query)
                    rows = result.fetchall()
                    dict_rows = [row._mapping for row in rows] # Cast to dict
                    LoggerMessageHelper.log_message(self.log_file, f"Fetched {len(dict_rows)} rows from source table '{table_name}'.")

                    with target_conn.begin() as transaction:
                        target_conn.execute(target_metadata.tables[table_name].insert(), dict_rows)
                        LoggerMessageHelper.log_message(self.log_file, f"Inserted {len(dict_rows)} rows into target table '{table_name}'.")

                        transaction.commit()
                        LoggerMessageHelper.log_message(self.log_file, f"Transaction committed.")

                LoggerMessageHelper.log_message(self.log_file, f"Table '{table_name}' has been replicated from '{db_name}' to '{db_name}'.")
                LoggerMessageHelper.log_message(self.log_file, "--- %s seconds ---" % (time.time() - start_time))

        except Exception as e:
            full_traceback = traceback.format_exc()
            logging.error(f'except error: {full_traceback}')

            LoggerMessageHelper.log_message(self.log_file, f'except error: {full_traceback}')

        finally:
            print('Finish')
            LoggerMessageHelper.log_message(self.log_file, 'Finish')

            return {
                'status': True,
                'msg': 'Finish'
            }
