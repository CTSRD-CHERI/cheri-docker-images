#!/bin/sh
set -e
# Work around docker-created volumes always being owned by root
chown -Rv gcc-user:users /compiler-explorer/lib/storage/data
cd /compiler-explorer
SUDO="sudo -u gcc-user --preserve-env=NODE_ENV"
$SUDO id
$SUDO make "$@"
