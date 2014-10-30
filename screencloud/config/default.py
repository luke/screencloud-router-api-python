# It is expected that the settings in here will be overridden in the file 
# ./local.py (note that in production, local.py is generated by confd)

DEBUG = False
SQL_DB_URI = '' # 'postgresql://screencloud:screencloud@localhost/screencloud'
REDIS_DB_URI = '' # 'redis://localhost:6379/0'
PUBSUB_URI = '' # 'https://screencloud.firebaseio.com/'
PUBSUB_SECRET = '' # 'some_firebase_secret'
