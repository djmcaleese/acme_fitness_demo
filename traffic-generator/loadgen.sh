#!/bin/bash
set -e

if [[ -z "${FRONTEND_ADDR}" ]]; then
    echo >&2 "FRONTEND_ADDR not specified"
    exit 1
fi

trap "exit" TERM
set -x

locust --host ${FRONTEND_ADDR} --users "${USERS:-10}" --spawn-rate "${SPAWN_RATE:-100}" --headless
