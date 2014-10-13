screencloud-router-api-python
=============================

Getting Started
---------------

To run the dev server: `python ./scripts/wsgi.py`

For this to work, you will need to have local settings defined in
(`screencloud/config/local.py`).

Alternatively, if you have confd installed (or are running from the docker
build):

    DEBUG=True SQL_DB_URI='blah' REDIS_DB_URI='blah' ... ./scripts/run.sh

That will use confd to build a `local.py` settings file from the environment
variables.  Note that the construction of `local.py` is governed by the files in
`/config/templates/`.  Production will try to read config from etcd:

    CONFD_BACKEND=etcd ./scripts/run.sh

