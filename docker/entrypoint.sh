#!/bin/bash
set -e

# inicia o webserver:
cd /app
gunicorn --paste production.ini -w 4 -b 0.0.0.0 --error-logfile=/var/log/access_api_gunicorn.log --access-logfile=/var/log/access_api_access.log --daemon

# inicia o thirft server
accessstats_thriftserver --port 11620 --host 0.0.0.0