from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import sessionmaker

from screencloud import config

engine = sqlalchemy_create_engine(
    config['SQL_DB_URI'],
    client_encoding='utf8'
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
