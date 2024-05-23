import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

class ETLRepository():
    def get_source_engine(db_name):
        return f"mysql+pymysql://{os.getenv('DB_ORIGIN_USERNAME')}:{os.getenv('DB_ORIGIN_PASSWORD')}@{os.getenv('DB_ORIGIN_HOST')}/{db_name}"

    def get_target_engine(db_name):
        return f"mysql+pymysql://{os.getenv('DB_TARGET_USERNAME')}:{os.getenv('DB_TARGET_PASSWORD')}@{os.getenv('DB_TARGET_HOST')}/{db_name}"

    def get_all_tables(db_name):
        db_url = ETLRepository.get_source_engine(db_name)

        engine = create_engine(db_url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        return tables
