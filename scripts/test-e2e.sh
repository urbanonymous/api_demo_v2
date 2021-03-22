#! /usr/bin/env sh

set -e
set -x

docker exec -it api-demo-v2 bash -c 'cd .. ; pytest tests_e2e/'
