import sys, os
sys.path.append(os.path.realpath(os.pardir))

import router_api
from router_api import models

def main():
    print('You asked for it.  Dropping and re-creating all tables...')
    models.Base.metadata.drop_all(bind=router_api.db_engine)
    models.Base.metadata.create_all(bind=router_api.db_engine)

if __name__ == '__main__':
    main()
