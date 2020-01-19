#!/bin/bash
set -eo pipefail
PARENT_DIR="$(cd "$(dirname "${0}")" ; pwd)"
# shellcheck source=/dev/null
. "${PARENT_DIR}/utils.sh"

if [ -d ~/.venv ]
then
    echo "Virtual environment restored from cache"
else
    ensure_venv_exists "${1}"
fi

if [ -d ~/package-cache ]
then
    echo "Package cache restore from cache"
    pip download --progress-bar=off --dest=./ --no-deps       \
        /tmp/workspace/dockerfixtures*.whl
else
    mkdir ~/package-cache
    pip download --progress-bar=off                           \
        --dest=~/package-cache                                \
        /tmp/workspace/dockerfixtures*.whl
    # Our package we do not want to cache only its dependencies
    rm ~/package-cache/dockerfixtures*.whl
    # Install everything, but our package
    pip install --progress-bar=off ~/package-cache/*
fi
