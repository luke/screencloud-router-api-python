import sys, os
sys.path.append(os.path.realpath(os.pardir))

from werkzeug.serving import run_simple
from screencloud.api import app

# Dev server
def main():
    wsgi_app = app.create_wsgi_app('screencloud')
    run_simple('', 5000, wsgi_app, use_reloader=True)

if __name__ == '__main__':
    main()
