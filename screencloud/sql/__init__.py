from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .. import config

def create_engine():
    return sqlalchemy_create_engine(
        config['SQLALCHEMY_DATABASE_URI'],
        convert_unicode=True
    )

def create_session():
    engine = create_engine()
    return scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
