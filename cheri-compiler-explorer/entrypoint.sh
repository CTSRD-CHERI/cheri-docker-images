#!/bin/sh
set -e
# Work around docker-created volumes always being owned by root
chown -Rv gcc-user:users /compiler-explorer/lib/storage/data
cd /compiler-explorer
sudo -u gcc-user id
sudo -u gcc-user make "$@"