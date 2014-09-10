import sys, os
sys.path.append(os.path.realpath(os.pardir))

import screencloud.api
import screencloud.config

def main():
    api = screencloud.api.create('screencloud')
    api.run(debug=screencloud.config['DEBUG'], use_reloader=True)

if __name__ == '__main__':
    main()
