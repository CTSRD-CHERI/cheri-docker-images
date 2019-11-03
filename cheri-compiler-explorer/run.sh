#!/bin/sh

git pull --rebase --autostash
mkdir -p ~/appdata/letsencrypt/config/nginx/site-confs/
cp -f nginx.conf ~/appdata/letsencrypt/config/nginx/site-confs/default
/usr/local/bin/docker-compose up -d --force-recreate --remove-orphans