import sys, os
sys.path.append(os.path.realpath(os.pardir))

from werkzeug.serving import run_simple
from screencloud import api

# Dev server
def main():
    app = api.create_app('screencloud')
    run_simple('', 5000, app, use_reloader=True)

if __name__ == '__main__':
    main()
