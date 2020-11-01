#!/usr/bin/env bash

set -xe

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir -p /root/appdata/letsencrypt/nginx/site-confs/
cp -f "${DIR}/nginx.conf" /root/appdata/letsencrypt/nginx/site-confs/default
cp -f "${DIR}/cheri-compiler-explorer.service" /etc/systemd/system/cheri-compiler-explorer.service
cp -f "${DIR}/email-on-failure@.service" /etc/systemd/system/email-on-failure@.service
cp -f "${DIR}/docker-cleanup.service" "${DIR}/docker-cleanup.timer" /etc/systemd/system/
systemctl daemon-reload
systemctl enable cheri-compiler-explorer.service
systemctl start cheri-compiler-explorer.service
systemctl enable docker-cleanup.timer
systemctl start docker-cleanup.timer
