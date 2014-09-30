# It is expected that the settings in here will be overridden in the file 
# ./local.py 

DEBUG = False
SQLALCHEMY_DATABASE_URI = '' # 'postgresql://screencloud:screencloud@localhost/screencloud'
REDIS = {} # {'host': 'localhost', 'port': 6379, 'db': 0}
OAUTH_CLIENTS = {}
# OAUTH_CLIENTS = {
#     'google': {
#         'client_id':'blah.apps.googleusercontent.com',
#         'client_secret':'secret',
#     }
# }
