#!/bin/bash
set -eo pipefail

if [ -d ~/.venv ]
then
    echo "Virtual environment restored from cache"
else
    python -m venv ~/.venv
    # shellcheck source=/dev/null
    . ~/.venv/bin/activate
    pip install -U pip  # 3.6 does not support --progress-bar out of the box
    pip install --progress-bar=off build "setuptools_scm[toml]~=6.0.0" twine
    # pip install --progress-bar=off -e '.[dev]'
fi
