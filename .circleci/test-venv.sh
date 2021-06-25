#!/bin/bash
set -eo pipefail
PARENT_DIR="$(cd "$(dirname "${0}")" ; pwd)"
# shellcheck source=/dev/null
. "${PARENT_DIR}/utils.sh"

# if [ -d ~/.venv ]
# then
#     echo "Virtual environment restored from cache"
# else
ensure_venv_exists "${1}"
pip3 install --progress-bar=off -U pip~=21.1.0 setuptools~=57.0.0 wheel~=0.36.2 setuptools_scm~=6.0.0
pip3 install --progress-bar=off -U -e .[dev]
# fi
