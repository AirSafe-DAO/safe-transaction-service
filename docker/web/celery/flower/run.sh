#!/bin/bash

set -euo pipefail
sleep 60

echo "==> $(date +%H:%M:%S) ==> Running Celery flower <=="
exec celery -C -A config.celery_app flower