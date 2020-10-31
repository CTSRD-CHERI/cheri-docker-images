#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir -p /root/appdata/letsencrypt/nginx/site-confs/
cp -f "${DIR}/nginx.conf" /root/appdata/letsencrypt/nginx/site-confs/default
cp -f "${DIR}/cheri-compiler-explorer.service" /etc/systemd/system/cheri-compiler-explorer.service
systemctl daemon-reload
systemctl enable cheri-compiler-explorer.service
systemctl start cheri-compiler-explorer.service
