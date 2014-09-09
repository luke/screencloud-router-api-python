import sys, os
sys.path.append(os.path.realpath(os.pardir))

import router_api

def main():
    router_api.app.run()

if __name__ == '__main__':
    main()
