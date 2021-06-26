#!/bin/bash
set -eo pipefail

if [ -d ~/.venv ]
then
    echo "Virtual environment restored from cache"
else
    python -m venv ~/.venv
    # shellcheck source=/dev/null
    . ~/.venv/bin/activate
    if [ "3.6" = "${1}" ]
    then
        pip install -U pip  # 3.6 does not support --progress-bar out of the box
    fi
    pip install --progress-bar=off build "setuptools_scm[toml]~=6.0.0"
    # pip install --progress-bar=off -e '.[dev]'
fi
