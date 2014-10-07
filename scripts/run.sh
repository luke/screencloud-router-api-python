#!/bin/bash

set -eo pipefail

# The directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[screencloud-router-api] Booting up..."

# Construct confd commandline (using env (default) or etcd as the backend).
CONFD_BACKEND=${CONFD_BACKEND:-"env"}
if [[ $CONFD_BACKEND == "etcd" ]]; then
  # If using etcd assume it's running on default docker0 (TODO)
  CONFD_BACKEND="etcd -node 172.17.42.1:4001"
fi
CONFD_CMD="confd -backend $CONFD_BACKEND -confdir ${DIR}/../config"

echo "[screencloud-router-api] Configuration backend: $CONFD_BACKEND"

# Try to generate configuration settings every 2 seconds until successful.
echo "[screencloud-router-api] Waiting for confd to create local settings..."
until $CONFD_CMD -onetime; do
  sleep 2
done
echo "[screencloud-router-api] Config complete."

# Start the api service
echo "[screencloud-router-api] Starting wsgi server..."
gunicorn --bind=:5000 --workers=1 wsgi:application --log-file=- --access-logfile=-
