#!/bin/sh

set -xe

git pull --rebase --autostash
mkdir -p ~/appdata/letsencrypt/nginx/site-confs/
cp -f nginx.conf ~/appdata/letsencrypt/nginx/site-confs/default
/usr/local/bin/docker-compose up -d --force-recreate --remove-orphans