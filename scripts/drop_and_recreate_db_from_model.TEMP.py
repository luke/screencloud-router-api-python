import sys, os
sys.path.append(os.path.realpath(os.pardir))

import screencloud
from screencloud import models

def main():
    print('You asked for it.  Dropping and re-creating all tables...')
    models.Base.metadata.drop_all(bind=screencloud.db_engine)
    models.Base.metadata.create_all(bind=screencloud.db_engine)

if __name__ == '__main__':
    main()
