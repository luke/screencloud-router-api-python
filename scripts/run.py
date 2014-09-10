import sys, os
sys.path.append(os.path.realpath(os.pardir))

from werkzeug.serving import run_simple
import screencloud.api

# Dev server
def main():
    server = screencloud.api.create_server('screencloud')
    run_simple('', 5000, server.wsgi_app, use_reloader=True)

if __name__ == '__main__':
    main()
