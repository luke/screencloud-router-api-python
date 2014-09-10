import sys, os
sys.path.append(os.path.realpath(os.pardir))

import screencloud

def main():
    api = screencloud.api.create('screencloud')
    api.run(debug=screencloud.config['DEBUG'])

if __name__ == '__main__':
    main()
