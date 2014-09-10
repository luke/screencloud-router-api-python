from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import config
from . import api

# Setup config 
config = config.to_dict()

# Setup the db connection
db_engine = create_engine(
    config['SQLALCHEMY_DATABASE_URI'], 
    convert_unicode=True
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
)

# TODO: Tidy up connection
