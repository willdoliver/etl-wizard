import os
import traceback, logging
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

from api.helpers.logger_message_helper import LoggerMessageHelper
from dotenv import load_dotenv

load_dotenv()

class ETLController():

    def sync_data(self):
        log_file = 'logs/log_etl_' + datetime.now().strftime("%Y_%m_%d") + '.log'
        LoggerMessageHelper.log_message(log_file, 'Sync Data Started')

        # Check database/tables to run ETL
        try:
            print('lets the etl begin')

        except Exception as e:
            full_traceback = traceback.format_exc()
            logging.error(f'except error: {full_traceback}')

            LoggerMessageHelper.log_message(log_file, f'except error: {full_traceback}')

        finally:
            print('Finish')
            LoggerMessageHelper.log_message(log_file, 'Finish')
            return {
                'status': True,
                'msg': 'Finish'
            }
    
    def extract(self, database: str, table_name: str) -> pd.DataFrame:
        print('extract data')

    def transform(self: pd.DataFrame) -> pd.DataFrame:
        print('transform data')

    def load(self) -> bool:
        print('load data')
