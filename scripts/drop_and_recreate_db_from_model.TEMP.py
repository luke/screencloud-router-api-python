import sys, os
sys.path.append(os.path.realpath(os.pardir))

from screencloud import sql
from screencloud.sql import models

def main():
    print('You asked for it.  Dropping and re-creating all tables...')
    engine = sql.create_engine()
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    main()
