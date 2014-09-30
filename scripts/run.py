import sys, os
if os.path.basename(os.path.realpath(os.curdir)) == 'scripts':
    sys.path.append(os.path.realpath(os.pardir))
elif os.path.exists(os.path.join(os.curdir, 'screencloud')):
    sys.path.append(os.path.realpath(os.curdir))
else:
    print 'Please run this from the scripts folder or the project root.'
    exit(1001)

from werkzeug.serving import run_simple
from screencloud.api import app

#: The wsgi app...
wsgi_app = app.create_wsgi_app('screencloud')

# Dev server
def main():
    run_simple('', 5000, wsgi_app, use_reloader=True)

if __name__ == '__main__':
    main()
