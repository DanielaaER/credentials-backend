from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv


class DatabaseSingleton:

    _instance = None  
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            
            load_dotenv()
            DB_USER = os.getenv("DEV_DB_USER")
            DB_PASSWORD = os.getenv("DEV_DB_PASS")
            DB_HOST = os.getenv("DEV_DB_HOST")
            DB_PORT = os.getenv("DEV_DB_PORT")
            DB_NAME = os.getenv("DEV_DB_NAME")
            print(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
            cls._instance.metadata = MetaData()
            cls._instance.Base = declarative_base()

        return cls._instance  
db_singleton = DatabaseSingleton()

SessionLocal = db_singleton.SessionLocal
Base = db_singleton.Base
meta_data = db_singleton.metadata
engine = db_singleton.engine
conn = engine.connect()